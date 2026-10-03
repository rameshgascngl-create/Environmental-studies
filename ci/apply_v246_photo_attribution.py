#!/usr/bin/env python3
from pathlib import Path
import json

MANIFEST = Path("../../ci/v246_visual_photo_manifest.json")
RAW_CREDITS = Path("app/src/main/res/raw/v246_photo_credits.json")
SCREEN = Path("app/src/main/java/edu/gascnagercoil/environmentalsciences/ui/LicencesScreen.kt")
AUDIT = Path("V246_PHOTO_ATTRIBUTION_AUDIT.json")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
assert len(manifest) == 8, len(manifest)
assert len({x["id"] for x in manifest}) == 8

required = (
    "id", "source_title", "author", "source_page", "license",
    "license_url", "modification_notice",
)
credits = []
for item in manifest:
    missing = [k for k in required if not str(item.get(k, "")).strip()]
    assert not missing, (item.get("id"), missing)
    assert item["id"].startswith("fig_v246_"), item["id"]
    assert item["output_ext"] == ".webp", item["id"]
    assert item["modification_notice"] == "resized and converted to WebP", item["id"]
    share_alike = "BY-SA" in item["license"]
    notice = item.get("share_alike_notice")
    if share_alike:
        assert notice and "ShareAlike" in notice, item["id"]
    else:
        assert notice in (None, ""), (item["id"], notice)
    credits.append({
        "id": item["id"],
        "title": item["source_title"],
        "author": item["author"],
        "sourceUrl": item["source_page"],
        "licence": item["license"],
        "licenceUrl": item["license_url"],
        "modification": item["modification_notice"],
        "shareAlikeNotice": notice or "",
    })

RAW_CREDITS.parent.mkdir(parents=True, exist_ok=True)
RAW_CREDITS.write_text(
    json.dumps(credits, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

before = SCREEN.read_text(encoding="utf-8")
assert "AndroidSVG 1.4" in before
assert "Noto Sans Tamil" in before

kotlin = r'''package edu.gascnagercoil.environmentalsciences.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import edu.gascnagercoil.environmentalsciences.R
import org.json.JSONArray

private data class PhotoCredit(
    val id: String,
    val title: String,
    val author: String,
    val sourceUrl: String,
    val licence: String,
    val licenceUrl: String,
    val modification: String,
    val shareAlikeNotice: String,
)

@Composable
internal fun LicencesScreen() {
    val context = LocalContext.current
    val uriHandler = LocalUriHandler.current
    val androidSvg = remember(context) {
        context.resources.openRawResource(R.raw.androidsvg_apache_2_license)
            .bufferedReader().use { it.readText() }
    }
    val noto = remember(context) {
        context.resources.openRawResource(R.raw.noto_sans_tamil_ofl)
            .bufferedReader().use { it.readText() }
    }
    val photoCredits = remember(context) {
        val raw = context.resources.openRawResource(R.raw.v246_photo_credits)
            .bufferedReader().use { it.readText() }
        val arr = JSONArray(raw)
        (0 until arr.length()).map { index ->
            val item = arr.getJSONObject(index)
            PhotoCredit(
                id = item.getString("id"),
                title = item.getString("title"),
                author = item.getString("author"),
                sourceUrl = item.getString("sourceUrl"),
                licence = item.getString("licence"),
                licenceUrl = item.getString("licenceUrl"),
                modification = item.getString("modification"),
                shareAlikeNotice = item.optString("shareAlikeNotice"),
            )
        }
    }

    LazyColumn(
        contentPadding = PaddingValues(18.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Text("Open-source licences", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text("திறந்த மூல உரிமங்கள்", style = MaterialTheme.typography.titleLarge)
            Text("AndroidSVG 1.4 — Apache License 2.0", fontWeight = FontWeight.SemiBold)
            Text("Noto Sans Tamil — SIL Open Font License 1.1", fontWeight = FontWeight.SemiBold)
        }
        item { Text(androidSvg, style = MaterialTheme.typography.bodySmall) }
        item { HorizontalDivider() }
        item { Text(noto, style = MaterialTheme.typography.bodySmall) }
        item { HorizontalDivider() }
        item {
            Text(
                "Photograph attributions / புகைப்பட உரிமக் குறிப்புகள்",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
            Text(
                "The following eight lesson photographs remain credited in their captions. " +
                    "Each copy used by this app was resized and converted to WebP.",
                style = MaterialTheme.typography.bodyMedium,
            )
        }
        items(photoCredits, key = { it.id }) { credit ->
            ElevatedCard(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    Text(credit.title, fontWeight = FontWeight.SemiBold)
                    Text("Author: " + credit.author)
                    Text("Source URL: " + credit.sourceUrl, style = MaterialTheme.typography.bodySmall)
                    Text("Licence: " + credit.licence)
                    Text("Licence URL: " + credit.licenceUrl, style = MaterialTheme.typography.bodySmall)
                    Text(credit.modification)
                    if (credit.shareAlikeNotice.isNotBlank()) {
                        Text(
                            "ShareAlike notice: " + credit.shareAlikeNotice,
                            style = MaterialTheme.typography.bodySmall,
                            fontWeight = FontWeight.Medium,
                        )
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        TextButton(onClick = { uriHandler.openUri(credit.sourceUrl) }) {
                            Text("Source page")
                        }
                        TextButton(onClick = { uriHandler.openUri(credit.licenceUrl) }) {
                            Text("Licence text")
                        }
                    }
                }
            }
        }
    }
}
'''
SCREEN.write_text(kotlin, encoding="utf-8")

screen = SCREEN.read_text(encoding="utf-8")
for credit in credits:
    assert credit["sourceUrl"] in RAW_CREDITS.read_text(encoding="utf-8")
assert "R.raw.v246_photo_credits" in screen
assert "Licence text" in screen
assert "resized and converted to WebP" in RAW_CREDITS.read_text(encoding="utf-8")

share_alike_ids = [x["id"] for x in credits if x["shareAlikeNotice"]]
AUDIT.write_text(
    json.dumps({
        "scope": "v2.4.6 photograph attribution and licence disclosure",
        "photoCreditCount": len(credits),
        "creditIds": [x["id"] for x in credits],
        "licencesScreenReadsPackagedCredits": True,
        "sourceLinksClickable": True,
        "licenceTextLinksClickable": True,
        "modificationNoticeExact": "resized and converted to WebP",
        "shareAlikeCreditIds": share_alike_ids,
        "shareAlikeNoticeCount": len(share_alike_ids),
        "versionIdentifiersChanged": False,
        "status": "PASS",
    }, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(AUDIT.read_text(encoding="utf-8"))
