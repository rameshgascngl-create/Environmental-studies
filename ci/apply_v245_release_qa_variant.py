#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

GRADLE = Path("app/build.gradle.kts")
QA_MANIFEST = Path("app/src/releaseQa/AndroidManifest.xml")
QA_TEST = Path("app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/ReleaseQaLessonEvidenceTest.kt")
AUDIT = Path("V245_RELEASE_QA_VARIANT_AUDIT.json")
LABEL = "QA-ONLY, DEBUG-SIGNED, NOT FOR DISTRIBUTION"

before = GRADLE.read_text(encoding="utf-8")
before_sha = hashlib.sha256(before.encode()).hexdigest()

production_guard = '''val releaseRequested = gradle.startParameter.taskNames.any { requested ->
    requested.endsWith("assembleRelease", ignoreCase = true) || requested.endsWith("bundleRelease", ignoreCase = true)
}
if (releaseRequested) {
    if (privacyPolicyUrl.get().isBlank()) throw GradleException("PRIVACY_POLICY_URL must be supplied for a release build.")
    if (!hasReleaseSigning && !allowUnsignedReleaseQa.get()) throw GradleException("Original Environmental Studies release signing credentials are required; do not generate a replacement key.")
}
'''
assert before.count(production_guard) == 1, "Production signing guard changed unexpectedly"

release_block = '''        release {
            isDebuggable = false
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            if (hasReleaseSigning) signingConfig = signingConfigs.getByName("release")
        }
'''
assert before.count(release_block) == 1, "Release build type not found exactly once"

qa_block = release_block + '''        create("releaseQa") {
            initWith(getByName("release"))
            isDebuggable = true
            isMinifyEnabled = true
            isShrinkResources = true
            signingConfig = signingConfigs.getByName("debug")
            matchingFallbacks += listOf("release")
        }
'''

after = before.replace(release_block, qa_block, 1)
build_types_marker = "    buildTypes {\n"
assert after.count(build_types_marker) == 1
after = after.replace(build_types_marker, '    testBuildType = "releaseQa"\n\n' + build_types_marker, 1)

assert after.count(production_guard) == 1
qa_section = after.split('create("releaseQa") {', 1)[1].split('}', 1)[0]
assert 'applicationIdSuffix' not in qa_section
assert 'isMinifyEnabled = true' in qa_section
assert 'isShrinkResources = true' in qa_section
assert 'signingConfig = signingConfigs.getByName("debug")' in qa_section
GRADLE.write_text(after, encoding="utf-8")

QA_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
QA_MANIFEST.write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">
    <application
        android:label="{LABEL}"
        tools:replace="android:label">
        <meta-data
            android:name="edu.gascnagercoil.environmentalsciences.RELEASE_QA_LABEL"
            android:value="{LABEL}" />
    </application>
</manifest>
''', encoding="utf-8")

QA_TEST.parent.mkdir(parents=True, exist_ok=True)
QA_TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences.qa

import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.os.SystemClock
import android.view.accessibility.AccessibilityNodeInfo
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.io.File
import java.io.FileOutputStream
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ReleaseQaLessonEvidenceTest {
    private val label = "QA-ONLY, DEBUG-SIGNED, NOT FOR DISTRIBUTION"

    @Test
    fun captureOpenParityEnglishLessonFigures() {
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val context = instrumentation.targetContext
        val packageName = context.packageName
        assertEquals("edu.gascnagercoil.environmentalsciences", packageName)
        assertEquals(label, context.applicationInfo.loadLabel(context.packageManager).toString())
        assertTrue(
            "releaseQa must remain debuggable for QA evidence extraction",
            context.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE != 0,
        )

        val out = File(context.filesDir, "releaseqa-evidence").apply {
            deleteRecursively()
            mkdirs()
        }

        val cases = listOf(
            Case(2, "u2l1", 5, "Energy enters ecosystems and nutrients are recycled", "u2l1-en-fig005.png", "u2l1_fig005_visible"),
            Case(2, "u2l5", 5, "The water cycle connects atmosphere, land and water", "u2l5-en-fig013.png", "u2l5_fig013_visible"),
            Case(4, "u4l6", 5, "Waste hierarchy: prevention before disposal", "u4l6-en-fig038.png", "u4l6_fig038_visible"),
            Case(5, "u5l1", 6, "Simplified greenhouse effect", "u5l1-en-fig046.png", "u5l1_fig046_visible"),
        )

        val status = mutableListOf(
            "variant=releaseQa",
            "label=$label",
            "applicationId=$packageName",
            "debuggable=true",
        )

        for (item in cases) {
            context.getSharedPreferences("learning_state", Context.MODE_PRIVATE)
                .edit()
                .putString("last_route", "lesson:${item.unit}:${item.lessonId}")
                .putString("language", "ENGLISH")
                .putInt("lesson_scroll_${item.unit}_${item.lessonId}_ENGLISH", item.scrollIndex)
                .commit()

            instrumentation.uiAutomation.executeShellCommand("am force-stop $packageName").close()
            val launch = context.packageManager.getLaunchIntentForPackage(packageName)
            assertNotNull("Launch intent missing", launch)
            launch!!.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
            context.startActivity(launch)

            assertTrue(
                "Expected figure title was not visible in ${item.lessonId}: ${item.expectedTitle}",
                waitForVisibleText(instrumentation, item.expectedTitle, 8000L),
            )

            val bitmap = instrumentation.uiAutomation.takeScreenshot()
            assertNotNull("Unable to capture ${item.lessonId}", bitmap)
            assertTrue(bitmap!!.width > 0 && bitmap.height > 0)
            val png = File(out, item.fileName)
            FileOutputStream(png).use {
                assertTrue(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, it))
            }
            assertTrue("${item.lessonId} screenshot is unexpectedly small", png.length() > 10000L)
            bitmap.recycle()
            status += "${item.statusKey}=PASS"
        }

        File(out, "status.txt").writeText(status.joinToString("\n", postfix = "\n"))
    }

    private fun waitForVisibleText(
        instrumentation: android.app.Instrumentation,
        expected: String,
        timeoutMs: Long,
    ): Boolean {
        val end = System.currentTimeMillis() + timeoutMs
        while (System.currentTimeMillis() < end) {
            val root = instrumentation.uiAutomation.rootInActiveWindow
            if (root != null && treeContains(root, expected)) return true
            SystemClock.sleep(250)
        }
        return false
    }

    private fun treeContains(node: AccessibilityNodeInfo, expected: String): Boolean {
        val text = node.text?.toString().orEmpty()
        val description = node.contentDescription?.toString().orEmpty()
        if (text.contains(expected) || description.contains(expected)) return true
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            if (treeContains(child, expected)) return true
        }
        return false
    }

    private data class Case(
        val unit: Int,
        val lessonId: String,
        val scrollIndex: Int,
        val expectedTitle: String,
        val fileName: String,
        val statusKey: String,
    )
}
''', encoding="utf-8")

final_gradle = GRADLE.read_text(encoding="utf-8")
assert final_gradle.count(production_guard) == 1
AUDIT.write_text(json.dumps({
    "scope": "QA-only releaseQa device-evidence variant",
    "label": LABEL,
    "applicationId": "edu.gascnagercoil.environmentalsciences",
    "debugSigned": True,
    "debuggableForEvidenceExtraction": True,
    "minifyEnabled": True,
    "shrinkResources": True,
    "productionSigningGuardAltered": False,
    "replacementProductionKeyGenerated": False,
    "distributionAllowed": False,
    "testBuildType": "releaseQa",
    "gradleSha256Before": before_sha,
    "gradleSha256After": hashlib.sha256(final_gradle.encode()).hexdigest(),
    "evidenceTest": str(QA_TEST),
    "manifestOverlay": str(QA_MANIFEST),
}, indent=2) + "\n", encoding="utf-8")
print(AUDIT.read_text(encoding="utf-8"))
