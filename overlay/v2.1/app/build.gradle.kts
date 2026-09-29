import org.gradle.api.GradleException

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

val privacyPolicyUrl = providers.gradleProperty("PRIVACY_POLICY_URL").orElse("")
val releaseStoreFile = providers.environmentVariable("ENVSTUDIES_KEYSTORE_PATH").orNull
val releaseStorePassword = providers.environmentVariable("ENVSTUDIES_KEYSTORE_PASSWORD").orNull
val releaseKeyAlias = providers.environmentVariable("ENVSTUDIES_KEY_ALIAS").orNull
val releaseKeyPassword = providers.environmentVariable("ENVSTUDIES_KEY_PASSWORD").orNull
val hasReleaseSigning = listOf(releaseStoreFile, releaseStorePassword, releaseKeyAlias, releaseKeyPassword).all { !it.isNullOrBlank() }
val releaseRequested = gradle.startParameter.taskNames.any { requested ->
    requested.endsWith("assembleRelease", ignoreCase = true) || requested.endsWith("bundleRelease", ignoreCase = true)
}
if (releaseRequested) {
    if (privacyPolicyUrl.get().isBlank()) throw GradleException("PRIVACY_POLICY_URL must be supplied for a release build.")
    if (!hasReleaseSigning) throw GradleException("Original Environmental Studies release signing credentials are required; do not generate a replacement key.")
}

android {
    namespace = "edu.gascnagercoil.environmentalsciences"
    compileSdk = 36

    defaultConfig {
        applicationId = "edu.gascnagercoil.environmentalsciences"
        minSdk = 24
        targetSdk = 36
        versionCode = 20100
        versionName = "2.1.0"
        buildConfigField("String", "PRIVACY_POLICY_URL", "\"${privacyPolicyUrl.get().replace("\"", "\\\"")}\"")
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    if (hasReleaseSigning) {
        signingConfigs {
            create("release") {
                storeFile = file(releaseStoreFile!!)
                storePassword = releaseStorePassword
                keyAlias = releaseKeyAlias
                keyPassword = releaseKeyPassword
                enableV1Signing = true
                enableV2Signing = true
                enableV3Signing = true
                enableV4Signing = true
            }
        }
    }

    buildTypes {
        debug {
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            if (hasReleaseSigning) signingConfig = signingConfigs.getByName("release")
        }
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
    packaging {
        resources.excludes += setOf("/META-INF/{AL2.0,LGPL2.1}")
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlin {
        compilerOptions {
            jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
        }
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2025.10.01")
    implementation(composeBom)
    androidTestImplementation(composeBom)
    implementation("androidx.activity:activity-compose:1.11.0")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}

