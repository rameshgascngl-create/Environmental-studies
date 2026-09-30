# Environmental Studies v2.2.1 — Scientific-Visual Correction Register

## Scope
Correction-only scientific-art changes. The 64 existing PNG assets remain packaged and unchanged unless a display block was withdrawn because a corrected SVG now provides the same or better scientific explanation. No decorative visual expansion is introduced.

| Visual | Baseline defect | v2.2.1 correction | Scientific acceptance criterion |
|---|---|---|---|
| Soil contamination — EN/TA (`v22_u04_l44_*`) | Plant uptake was combined with “Food & drinking water”, conflating food-chain and groundwater exposure pathways. | Redrawn into three distinct pathways: contaminated soil → plant uptake → food/food-chain exposure; contaminated soil → leaching → groundwater → drinking-water exposure; contaminated soil → runoff/erosion → surface water/aquatic ecosystems. | No pathway implies plant uptake is the direct source of drinking water. |
| Biodiversity drivers — EN/TA (`v22_u03_l32_*`) | Five arrows converged on a central “Biodiversity” node, which could be read as supportive inputs. | Reframed as major direct pressures on biodiversity and central node changed to biodiversity loss/change. Drivers retained: land/sea-use change, direct exploitation, climate change, pollution, invasive alien species. | Direction and node semantics represent pressure/decline, not support. |
| Greenhouse effect — EN/TA (`v221_u05_l51_*`) | Existing PNG wording was visually attractive but scientifically vague. | Added a corrected SVG pair: incoming solar radiation → surface absorption/warming → outgoing infrared radiation → greenhouse-gas absorption and re-emission → part directed downward and part escaping to space. | Does not depict greenhouse gases as a rigid physical blanket; labels specify infrared absorption/re-emission. |
| Ozone depletion vs acid deposition — EN/TA (`v22_u05_l54_*`) | Tamil terminology varied and mechanism separation needed improvement. | Standardised **அமிலப் படிவு (Acid deposition)** and labels distinguish ozone-depletion chemistry from SO₂/NOₓ atmospheric transformation and wet/dry deposition. | Ozone depletion and acid deposition remain separate mechanisms; wet and dry deposition are explicit. |
| Sustainable water use — EN/TA (`v22_u06_l63_*`) | Baseline sequence looked like a strict linear cycle; Tamil labels were telegraphic. | Reworked as a strategy hierarchy/hub with natural Tamil imperatives: avoid waste, efficient use, safe reuse, rainwater/recharge, measure/monitor. | Does not imply all strategies must occur in one causal sequence. |
| Campus waste audit — TA (`v22_u09_l93_ta`) | Machine-like “மூலங்களை வரைபடு”, “காரணம் பகுப்பாய்வு”. | “கழிவு உருவாகும் இடங்களை வரைபடமிடு”; “காரணங்களைப் பகுப்பாய்வு செய்”. | Natural Tamil action language, readable at phone scale. |
| Water-use observation — TA (`v22_u09_l94_ta`) | Awkward compressed labels. | “நீர்ப் பயன்பாடு மற்றும் மழைநீர் கண்காணிப்பு”, “நீர் மூலங்களை அடையாளம் காண்”, “கசிவு மற்றும் வீணாக்கத்தை கண்டறி”. | Labels are grammatical and scientifically unambiguous. |
| Local environmental observation — TA (`v22_u09_l95_ta`) | “மனித அழுத்தம் பதிவு” was telegraphic. | “மனிதச் செயல்பாடுகளால் ஏற்படும் அழுத்தங்களைப் பதிவு செய்”. | Natural Tamil; anthropogenic-pressure meaning retained. |
| Campus action plan — TA (`v22_u09_l96_ta`) | “செயல் பொறுப்பு”, “குறியீடு கண்காணி” were compressed. | “செயல் மற்றும் பொறுப்பை நிர்ணயி”; “முன்னேற்றக் குறியீட்டைக் கண்காணி”. | Action/responsibility and monitoring remain conceptually distinct. |

## Figure parity policy
Separate duplicate resources are not required when the same scientific information is fully available in Tamil through the corresponding figure, caption or explanatory block. After correction, one intentional count exception remains in Lesson 4.2: Tamil includes an extra CPCB NAAQS reference figure while the English lesson provides the same regulatory values in textual reference form.

## Tamil SVG quality gate
Static checks verify XML parsing, local-only resources and Tamil Unicode presence. Physical-device acceptance is still mandatory for glyph shaping, ligatures, clipping, label collision, contrast, leader alignment and readability at normal scale and after tap-to-enlarge.
