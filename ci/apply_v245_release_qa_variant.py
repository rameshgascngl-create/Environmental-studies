#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

GRADLE = Path("app/build.gradle.kts")
QA_MANIFEST = Path("app/src/releaseQa/AndroidManifest.xml")
QA_TEST = Path("app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/ReleaseQaLessonEvidenceTest.kt")
SVG_QA_TEST = Path("app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/SvgAndroidSvgScreenshotTest.kt")
V246_SVG_QA_TEST = Path("app/src/androidTest/java/edu/gascnagercoil/environmentalsciences/qa/V246SvgAndroidSvgScreenshotTest.kt")
QA_TEST_PROGUARD = Path("app/proguard-releaseqa-androidtest.pro")
QA_TARGET_PROGUARD = Path("app/proguard-releaseqa-target.pro")
QA_RUNTIME_KEEP_SOURCE = Path("../../ci/v245_releaseqa_runtime_keep.pro")
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
            proguardFiles("proguard-releaseqa-target.pro")
            signingConfig = signingConfigs.getByName("debug")
            testProguardFiles("proguard-releaseqa-androidtest.pro")
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
assert 'proguardFiles("proguard-releaseqa-target.pro")' in qa_section
assert 'signingConfig = signingConfigs.getByName("debug")' in qa_section
assert 'testProguardFiles("proguard-releaseqa-androidtest.pro")' in qa_section
dependency_anchor = '    androidTestImplementation("androidx.test.ext:junit:1.2.1")\n'
assert after.count(dependency_anchor) == 1
after = after.replace(
    dependency_anchor,
    dependency_anchor
    + '    androidTestImplementation("com.google.errorprone:error_prone_annotations:2.36.0")\n'
    + '    androidTestImplementation(kotlin("stdlib"))\n',
    1,
)
GRADLE.write_text(after, encoding="utf-8")

exact_runtime_rules = QA_RUNTIME_KEEP_SOURCE.read_text(encoding="utf-8")
assert "-keep class kotlin.LazyKt { *; }" in exact_runtime_rules
assert "-keep class kotlin.io.FilesKt { *; }" in exact_runtime_rules
assert "-keep class androidx.test.platform.app.InstrumentationRegistry { *; }" in exact_runtime_rules
assert "-keep class kotlinx.coroutines.test.TestCoroutineScheduler { *; }" in exact_runtime_rules
assert "-keep class kotlin.**" not in exact_runtime_rules
assert "-keep class kotlinx.**" not in exact_runtime_rules
assert "-keep class androidx.test.**" not in exact_runtime_rules

QA_TARGET_PROGUARD.write_text(
    "# QA-only releaseQa target R8 rules. Production release does not consume this file.\n"
    + exact_runtime_rules,
    encoding="utf-8",
)

QA_TEST_PROGUARD.write_text(
    "# QA-only AndroidTest R8 rules.\n"
    "# error_prone_annotations references JDK compiler model types that are not present on Android.\n"
    "-dontwarn javax.lang.model.element.**\n"
    + exact_runtime_rules,
    encoding="utf-8",
)

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

            // Do not force-stop the target package here. releaseQa instrumentation
            // executes in the target process, so force-stop terminates this harness.
            val launch = context.packageManager.getLaunchIntentForPackage(packageName)
            assertNotNull("Launch intent missing", launch)
            launch!!.addFlags(
                Intent.FLAG_ACTIVITY_NEW_TASK or
                    Intent.FLAG_ACTIVITY_CLEAR_TASK or
                    Intent.FLAG_ACTIVITY_CLEAR_TOP,
            )
            context.startActivity(launch)
            instrumentation.waitForIdleSync()

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


SVG_QA_TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences.qa

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.os.Build
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.caverock.androidsvg.SVG
import java.io.File
import java.io.FileOutputStream
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class SvgAndroidSvgScreenshotTest {
    @Test
    fun renderEveryTamilSvgThroughAndroidSvg() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val resources = context.resources
        val out = requireNotNull(context.getExternalFilesDir("svg-androidsvg")) {
            "External files directory unavailable for AndroidSVG evidence"
        }.apply {
            deleteRecursively()
            assertTrue("Unable to create external AndroidSVG evidence directory", mkdirs() || isDirectory)
        }

        val bookId = resources.getIdentifier("book_content", "raw", context.packageName)
        assertTrue("book_content raw resource lookup failed", bookId != 0)
        val book = resources.openRawResource(bookId)
            .bufferedReader(Charsets.UTF_8)
            .use { JSONObject(it.readText()) }

        val tamilSvgNames = linkedSetOf<String>()
        val units = book.getJSONArray("units")
        for (unitIndex in 0 until units.length()) {
            val lessons = units.getJSONObject(unitIndex).getJSONArray("lessons")
            for (lessonIndex in 0 until lessons.length()) {
                val lesson = lessons.getJSONObject(lessonIndex)
                val tamil = lesson.getJSONArray("tamil")
                for (blockIndex in 0 until tamil.length()) {
                    val block = tamil.getJSONObject(blockIndex)
                    if (block.optString("kind") == "svg_figure") {
                        val figure = block.optString("figure")
                        assertTrue(
                            "Tamil svg_figure block has an empty figure name in lesson " +
                                lesson.optString("id"),
                            figure.isNotBlank(),
                        )
                        tamilSvgNames += figure
                    }
                }
            }
        }

        val expected = 46
        assertEquals(
            "book_content.json must reference exactly 46 unique Tamil svg_figure resources",
            expected,
            tamilSvgNames.size,
        )

        val candidates = tamilSvgNames.sorted().map { name ->
            val resourceId = resources.getIdentifier(name, "raw", context.packageName)
            assertTrue(
                "Tamil svg_figure resource lookup failed through getIdentifier: $name",
                resourceId != 0,
            )
            name to resourceId
        }

        val rendered = mutableListOf<String>()
        for ((name, resourceId) in candidates) {
            val svg = resources.openRawResource(resourceId).use { SVG.getFromInputStream(it) }
            val picture = svg.renderToPicture(1600, 1000)
            assertTrue("AndroidSVG picture width is zero: $name", picture.width > 0)
            assertTrue("AndroidSVG picture height is zero: $name", picture.height > 0)

            val bitmap = Bitmap.createBitmap(
                picture.width,
                picture.height,
                Bitmap.Config.ARGB_8888,
            )
            val canvas = Canvas(bitmap)
            canvas.drawColor(Color.WHITE)
            canvas.drawPicture(picture)

            val png = File(out, "$name.png")
            FileOutputStream(png).use { stream ->
                assertTrue(
                    "PNG compression failed: $name",
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream),
                )
            }
            bitmap.recycle()

            assertTrue("Empty AndroidSVG screenshot: $name", png.length() > 256L)
            rendered += png.name
        }

        assertEquals("Every Tamil raw SVG must render", expected, rendered.size)
        val manifest = listOf(
            "api=${Build.VERSION.SDK_INT}",
            "package=${context.packageName}",
            "output=${out.absolutePath}",
            "expected=$expected",
            "rendered=${rendered.size}",
            "result=${rendered.size}/$expected",
        ) + rendered.map { "file=$it" }
        File(out, "result-manifest.txt").writeText(manifest.joinToString("\n", postfix = "\n"))
        assertTrue(File(out, "result-manifest.txt").length() > 0L)
    }
}
''', encoding="utf-8")


V246_SVG_QA_TEST.write_text(r'''package edu.gascnagercoil.environmentalsciences.qa

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.os.Build
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.caverock.androidsvg.SVG
import java.io.File
import java.io.FileOutputStream
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class V246SvgAndroidSvgScreenshotTest {
    @Test
    fun renderV246TamilSvgAtlasThroughAndroidSvg() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val resources = context.resources
        val out = requireNotNull(context.getExternalFilesDir("v246-svg-androidsvg")) {
            "External files directory unavailable for v2.4.6 AndroidSVG evidence"
        }.apply {
            deleteRecursively()
            assertTrue("Unable to create v2.4.6 AndroidSVG evidence directory", mkdirs() || isDirectory)
        }

        val bookId = resources.getIdentifier("book_content", "raw", context.packageName)
        assertTrue("book_content raw resource lookup failed", bookId != 0)
        val book = resources.openRawResource(bookId)
            .bufferedReader(Charsets.UTF_8)
            .use { JSONObject(it.readText()) }

        val names = linkedSetOf<String>()
        val units = book.getJSONArray("units")
        for (unitIndex in 0 until units.length()) {
            val lessons = units.getJSONObject(unitIndex).getJSONArray("lessons")
            for (lessonIndex in 0 until lessons.length()) {
                val lesson = lessons.getJSONObject(lessonIndex)
                val tamil = lesson.getJSONArray("tamil")
                for (blockIndex in 0 until tamil.length()) {
                    val block = tamil.getJSONObject(blockIndex)
                    if (block.optString("kind") != "svg_figure") continue
                    val figure = block.optString("figure")
                    if (figure.startsWith("sci_v246_") && figure.endsWith("_t")) {
                        names += figure
                    }
                }
            }
        }

        val expected = 56
        assertEquals(
            "v2.4.6 visual atlas must reference exactly 56 unique Tamil SVG resources",
            expected,
            names.size,
        )

        val candidates = names.sorted().map { name ->
            val resourceId = resources.getIdentifier(name, "raw", context.packageName)
            assertTrue("v2.4.6 Tamil SVG resource lookup failed: $name", resourceId != 0)
            name to resourceId
        }

        val rendered = mutableListOf<String>()
        for ((name, resourceId) in candidates) {
            val svg = resources.openRawResource(resourceId).use { SVG.getFromInputStream(it) }
            val picture = svg.renderToPicture(1600, 1000)
            assertTrue("AndroidSVG picture width is zero: $name", picture.width > 0)
            assertTrue("AndroidSVG picture height is zero: $name", picture.height > 0)

            val bitmap = Bitmap.createBitmap(
                picture.width,
                picture.height,
                Bitmap.Config.ARGB_8888,
            )
            val canvas = Canvas(bitmap)
            canvas.drawColor(Color.WHITE)
            canvas.drawPicture(picture)

            val png = File(out, "$name.png")
            FileOutputStream(png).use { stream ->
                assertTrue(
                    "PNG compression failed: $name",
                    bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, stream),
                )
            }
            bitmap.recycle()
            assertTrue("Empty AndroidSVG screenshot: $name", png.length() > 256L)
            rendered += png.name
        }

        assertEquals("Every v2.4.6 Tamil SVG must render", expected, rendered.size)
        val manifest = listOf(
            "api=${Build.VERSION.SDK_INT}",
            "package=${context.packageName}",
            "output=${out.absolutePath}",
            "expected=$expected",
            "rendered=${rendered.size}",
            "result=${rendered.size}/$expected",
        ) + rendered.map { "file=$it" }
        File(out, "result-manifest.txt").writeText(manifest.joinToString("\n", postfix = "\n"))
        assertTrue(File(out, "result-manifest.txt").length() > 0L)
    }
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
    "androidTestR8SupportDependency": "com.google.errorprone:error_prone_annotations:2.36.0",
    "androidTestKotlinStdlibDependency": "kotlin(\\\"stdlib\\\")",
    "releaseQaTargetR8Rules": str(QA_TARGET_PROGUARD),
    "releaseQaExactRuntimeKeepSource": str(QA_RUNTIME_KEEP_SOURCE),
    "releaseQaExactRuntimeKeepRuleCount": sum(
        1 for line in exact_runtime_rules.splitlines() if line.startswith("-keep class ")
    ),
    "releaseQaRun199MissingClassCount": 1365,
    "releaseQaRun199MissingClassNamespaces": {
        "androidx.test": 1234,
        "kotlin": 25,
        "kotlinx": 106,
    },
    "androidTestR8Rules": str(QA_TEST_PROGUARD),
    "androidTestR8DontWarn": "javax.lang.model.element.**",
    "productionKotlinKeepWildcardAdded": False,
    "gradleSha256Before": before_sha,
    "gradleSha256After": hashlib.sha256(final_gradle.encode()).hexdigest(),
    "evidenceTest": str(QA_TEST),
    "androidSvgEvidenceTest": str(SVG_QA_TEST),
    "v246AndroidSvgEvidenceTest": str(V246_SVG_QA_TEST),
    "v246AndroidSvgEvidenceOutput": "targetContext.getExternalFilesDir(\\\"v246-svg-androidsvg\\\")",
    "androidSvgEvidenceOutput": "targetContext.getExternalFilesDir(\\\"svg-androidsvg\\\")",
    "manifestOverlay": str(QA_MANIFEST),
}, indent=2) + "\n", encoding="utf-8")
print(AUDIT.read_text(encoding="utf-8"))
