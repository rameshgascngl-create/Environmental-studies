#!/usr/bin/env python3
from pathlib import Path

GRADLE = Path("app/build.gradle.kts")
text = GRADLE.read_text(encoding="utf-8")
marker = 'val privacyPolicyUrl = providers.gradleProperty("PRIVACY_POLICY_URL").orElse("")\n'
assert text.count(marker) == 1, "privacyPolicyUrl declaration not found exactly once"

block = r'''
val privacyPolicyUrlValue = privacyPolicyUrl.get().trim()

fun validateReleasePrivacyPolicyUrl(url: String) {
    if (url.isBlank()) {
        throw GradleException("PRIVACY_POLICY_URL must not be blank for a release build")
    }
    if (!url.startsWith("https://", ignoreCase = true)) {
        throw GradleException("PRIVACY_POLICY_URL must use HTTPS")
    }
    val lower = url.lowercase()
    val forbidden = listOf(
        "raw.githubusercontent.com",
        "/release/",
        "/refs/heads/",
        "/blob/",
        "/tree/",
    )
    if (forbidden.any(lower::contains)) {
        throw GradleException(
            "PRIVACY_POLICY_URL must be a stable public endpoint, not a raw or branch-specific URL"
        )
    }
}

val releaseTaskRequested = gradle.startParameter.taskNames.any {
    it.contains("Release", ignoreCase = true)
}
if (releaseTaskRequested) {
    validateReleasePrivacyPolicyUrl(privacyPolicyUrlValue)
}
'''.lstrip()

text = text.replace(marker, marker + block, 1)
GRADLE.write_text(text, encoding="utf-8")

verify = GRADLE.read_text(encoding="utf-8")
assert "validateReleasePrivacyPolicyUrl" in verify
assert "raw.githubusercontent.com" in verify
assert '"/release/"' in verify
assert '"/refs/heads/"' in verify
assert "releaseTaskRequested" in verify
print("Phase 2 offline-safe Privacy URL release lint installed.")
