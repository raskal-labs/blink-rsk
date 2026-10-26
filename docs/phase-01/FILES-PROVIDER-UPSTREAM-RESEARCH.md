# Files.app source and community research — October 26, 2026

**Scope:** research under issue #2 in response to the persistent Files pending-item stall. This is supporting evidence, not another roadmap or authorization to patch, build, reset a domain or replace the app. Existing source, installation and device results remain separate.

**Finding:** a compatible, one-line upstream File Provider change missing from our pin was found. It is a concrete backport candidate for review, not a demonstrated cure for the user's stalled item. No fully verified replacement fork for this exact SideStore/iOS setup was established.

## Concrete upstream change

[`7e28d1721ecb6614951040477036ef31d5a0964e`](https://github.com/blinksh/blink/commit/7e28d1721ecb6614951040477036ef31d5a0964e), authored April 23, 2026, is publicly retrievable by exact SHA. It changes only `BlinkFileProvider/FileProviderReplicatedExtension.swift`, commenting out the startup call to `cleanUpOldTmpFiles()`. Input blob `5a2e68107f52bd95f6c64c3b852ba6bed667c7bc` is exactly our pinned file; output is `9381403608eb952db0c399b65a4e0e02004514c2`. The timer for normal change polling remains enabled. The repair is absent from `a90b4423` and from the October 24 IPA's source patch scope.

The maintainer's [18.6.1 announcement](https://github.com/blinksh/blink/discussions/2244) describes disabling bootstrap operations that produced a persistent warning icon while file operations still worked. The announcement supports investigating startup cleanup, but its symptom is **(!)**, not this device's **Syncing 1 item**. Our code inspection shows that cleanup enumerates the remote root and removes old `.blink.tmp.*` files. This is a background operation that does not require a user copy/move. Whether it caused this pending item is **Unknown**. Do not manually remove temporary files or infer that this patch repairs a corrupted existing replica.

## Other discussions and reported solutions

| Source | Evidence | Applicability |
| --- | --- | --- |
| [#2033](https://github.com/blinksh/blink/issues/2033), November 2024 follow-up | A user reported that switching an existing location from legacy to Replicated did not work, but deleting/saving and recreating it as Replicated did. The maintainer reproduced the transition issue. For VeraCrypt, the configured root also needed to be inside the mount for temporary-file placement. | A reported success for a particular old-provider transition, not proof that a reset cures the current unidentified pending item. Our pin already creates Replicated locations only. |
| [#2236](https://github.com/blinksh/blink/discussions/2236) / [#2237](https://github.com/blinksh/blink/issues/2237) | Validation could stay on Connecting while SSH/Mosh/SCP worked. Maintainer confirmed and announced the fix in 18.6. | `d1ee516a948287c2f820bfb44455d84429e78dff` retains the validation connection; verified ancestor of our pin. Already included, and validation is distinct from transfer completion. |
| [#2051](https://github.com/blinksh/blink/issues/2051), [#1717](https://github.com/blinksh/blink/issues/1717) | Older iOS 18 provider problems motivated the Replicated API transition. | Our source already uses Replicated; the issue being open or a generic upgrade recommendation does not establish a missing repair. |
| [Official location-removal documentation](https://docs.blink.sh/advanced/files-app#how-to-delete-a-location) | Recreating a location resets its local replica and sync state, including pending local changes. | The documented reset route is supported, but it has a real data-loss boundary and is not itself an observed fix on this phone. No reset was performed by this research. |

## Fork source comparison

Compared **184 repository/ref directory snapshots across 105 forks**: the 100 newest public fork default refs fetched October 26, the 76 custom commit tips sampled October 23, and eight older-active branch refs. Compared all entries of `BlinkFileProvider`, with subtree SHAs covering its SSH directory. This differs from the earlier bookmark-manager-only audit.

- **161** provider directories matched our pin.
- **14** differed only by the startup-cleanup disable above, inherited from upstream.
- **1** changed new-empty-file creation permissions to `0666` so remote umask can apply. This is [ahmedalsudani commit `1cd2fe47`](https://github.com/ahmedalsudani/blink/commit/1cd2fe479bda85caa1c10139cffe56b1a7053ab9), not a demonstrated sync-hang fix.
- **4** were older provider variants in b-relay/CoultonF branches, including different queue/replay handling. b-relay `raw` is the older 18.3.0 source; these are not evidence of newer hang fixes. CoultonF's signing commits do not establish provider runtime acceptance.
- **4** paths were unavailable (three HermesLink selections and one other fork). A restructured or unavailable path is not proof an implementation is absent.

[Machine-readable comparisons and blob receipts](fileprovider-fork-audit-20261026.json) retain the precise sample and limitations. This is not an exhaustive audit of all forks, every custom branch, whole-app changes, provisioning or private fixes.

| Project | Reviewed source/evidence | Verdict |
| --- | --- | --- |
| [b-relay `brendon/main`](https://github.com/b-relay/blink/tree/862b32d34fc7c2a86968f2a8c48cb3c7eb39f12d), [madjinn `personal-testflight`](https://github.com/madjinn/blink/tree/a31aa977e297c9c4a2c3a54e6a3d9b191cf17a85) | Both contain exactly the upstream cleanup-disable change in their provider directory. | Useful repair provenance. No matching SideStore/iOS 27 browse/transfer/reopen/refresh acceptance found. Prefer reviewing the upstream one-line change over adopting either whole fork. |
| [Iroha / wg-dev-env](https://github.com/wg-dev-env/blink/commit/6de42fc7f42e18d687d12ce261de537a98cb9155) | Initial setup explicitly removes embedding of both File Provider extensions; later work adds a separate in-app SFTP browser. | Not a native Files.app replacement. |
| [Geistty's failure record](https://github.com/daiimus/geistty/blob/main/FILE_PROVIDER_LEARNINGS.md) | The author archived its provider after browsing/file operations worked but a persistent sync banner and state problems remained. | Related failure lessons about anchors, error handling and domain state; not a fixed Blink fork or a verified reset prescription for our phone. |

## Result and boundary

The strongest contained source lead is **upstream `7e28d172`**. Its compatibility and absence are established; its causal link to this phone's failure is not. Current acceptance remains **Blocked** for Files sync. Before implementation, any new work order should explicitly define the source patch, native validation, one additional candidate build if authorized, and device acceptance without discarding pending local data by default. Do not promote this research into a wholesale source upgrade, a new File Provider, or a fork switch.

No functional source was edited, no build dispatched, no signing identity changed and no phone/server operation performed. Unrelated local research remains preserved.
