from pathlib import Path

GRADLE = Path("app/build.gradle.kts")
text = GRADLE.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, found {count}")
    text = text.replace(old, new, 1)


replace_once(
    'import org.gradle.api.GradleException\n',
    'import org.gradle.api.GradleException\nimport java.util.Properties\n',
    "Properties import",
)

replace_once(
    '''val privacyPolicyUrl = providers.gradleProperty("PRIVACY_POLICY_URL").orElse("")
val releaseStoreFile = providers.environmentVariable("ENVSTUDIES_KEYSTORE_PATH").orNull
val releaseStorePassword = providers.environmentVariable("ENVSTUDIES_KEYSTORE_PASSWORD").orNull
val releaseKeyAlias = providers.environmentVariable("ENVSTUDIES_KEY_ALIAS").orNull
val releaseKeyPassword = providers.environmentVariable("ENVSTUDIES_KEY_PASSWORD").orNull
val hasReleaseSigning = listOf(releaseStoreFile, releaseStorePassword, releaseKeyAlias, releaseKeyPassword).all { !it.isNullOrBlank() }
''',
    '''val privacyPolicyUrl = providers.gradleProperty("PRIVACY_POLICY_URL").orElse("")

val localProperties = Properties().apply {
    val localPropertiesFile = rootProject.file("local.properties")
    if (localPropertiesFile.isFile) {
        localPropertiesFile.inputStream().use(::load)
    }
}

fun signingValue(localKey: String, environmentKey: String): String? {
    return localProperties.getProperty(localKey)?.takeIf { it.isNotBlank() }
        ?: localProperties.getProperty(environmentKey)?.takeIf { it.isNotBlank() }
        ?: providers.environmentVariable(environmentKey).orNull?.takeIf { it.isNotBlank() }
}

val releaseStoreFile = signingValue("envstudies.keystore.path", "ENVSTUDIES_KEYSTORE_PATH")
val releaseStorePassword = signingValue("envstudies.keystore.password", "ENVSTUDIES_KEYSTORE_PASSWORD")
val releaseKeyAlias = signingValue("envstudies.key.alias", "ENVSTUDIES_KEY_ALIAS")
val releaseKeyPassword = signingValue("envstudies.key.password", "ENVSTUDIES_KEY_PASSWORD")
val hasReleaseSigning = listOf(releaseStoreFile, releaseStorePassword, releaseKeyAlias, releaseKeyPassword).all { !it.isNullOrBlank() }
''',
    "release signing source",
)

replace_once(
    '''        release {
            isMinifyEnabled = true
            isShrinkResources = true
''',
    '''        release {
            isDebuggable = false
            isMinifyEnabled = true
            isShrinkResources = true
''',
    "explicit release hardening",
)

replace_once(
    '                storeFile = file(releaseStoreFile!!)\n',
    '                storeFile = rootProject.file(releaseStoreFile!!)\n',
    "keystore path resolution",
)

GRADLE.write_text(text, encoding="utf-8")

assert 'isDebuggable = false' in text
assert 'isMinifyEnabled = true' in text
assert 'isShrinkResources = true' in text
assert 'applicationIdSuffix = ".debug"' in text
release_block = text.split("release {", 1)[1].split("}", 1)[0]
assert "applicationIdSuffix" not in release_block
assert 'rootProject.file("local.properties")' in text
assert "ENVSTUDIES_KEYSTORE_PATH" in text
print("A1 release configuration hardened.")
