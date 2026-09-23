# Review: Technology & Digital Life, part B ([^197]-[^234])
Reviewed: 38/38. OK: 21. SOFTEN: 6. ARCHIVE: 11.

## [^199] PSA: Factory Resets Don't Make Your Android Phone Safe to Sell
**Verdict:** SOFTEN
**Reason:** The underlying 2014 Avast study is real, but Android has shipped full-disk encryption by default since Android 6.0 Marshmallow (2015) — a factory reset combined with a lock screen is now far more effective than when this article ran, so the blanket warning needs updated context.
**Find this exact text in the doc:**
"""
Selling or donating an Android phone requires more than just a factory reset: security researchers at Avast recovered a surprising amount of personal data from 20 supposedly "wiped" used smartphones, showing that the built-in factory reset option doesn't reliably erase everything[^199].
"""
**Replace with:**
"""
Selling or donating an Android phone benefits from more than just a factory reset: a 2014 study from security researchers at Avast recovered a surprising amount of personal data from 20 supposedly "wiped" used smartphones, though full-disk encryption has been standard on Android since 2015 (making a reset paired with a lock screen far more effective today) — it's still worth removing accounts and confirming encryption is on before selling or donating a device[^199].
"""

## [^200] Use Instant Rice When Reviving a Wet Phone, Not Uncooked Rice
**Verdict:** ARCHIVE
**Reason:** Apple's official 2024 support guidance now warns against using rice (of any kind) to dry a wet iPhone at all, citing the risk of rice particles damaging the device, and recommends tapping out liquid and air-drying instead — directly contradicting this tip's premise.
**Find this exact text in the doc:**
"""
For a phone that's taken an accidental swim, an experiment comparing different drying agents found that instant rice does a better job of reviving a wet phone than the traditional trick of burying it in uncooked rice[^200].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2014 tip compared drying agents for a water-damaged phone and concluded instant rice worked better than the traditional trick of burying it in uncooked rice. Apple's official guidance as of 2024 now advises against using any kind of rice at all — citing the risk of rice particles getting into and damaging the phone — and instead recommends gently tapping out liquid and letting the device air-dry. [^200]
"""

## [^201] Reboot Your iPhone Without Touching the Home or Power Button
**Verdict:** ARCHIVE
**Reason:** iOS has since added an official, simpler way to reboot without physical buttons (Settings > General > Shut Down, and "Hey Siri, restart iPhone"), making the 2015-era Accessibility/Bold Text workaround unnecessary and largely superseded.
**Find this exact text in the doc:**
"""
When the physical Home or Power buttons stop responding, an iPhone can still be rebooted by changing certain Accessibility or Network settings—such as enabling Bold Text—that trigger an automatic restart, with the Accessibility route preferred since it doesn't wipe saved Wi-Fi passwords the way a network reset does[^201].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2015 tip described rebooting a Home/Power-button-broken iPhone by toggling an Accessibility or Network setting (like Bold Text) to force an automatic restart. iOS has since added an official, much simpler way to do this — Settings > General > Shut Down, or asking Siri to restart the phone — making the old accessibility-setting workaround unnecessary. [^201]
"""

## [^202] Batch Delete Photos in iOS from the Moments Section
**Verdict:** ARCHIVE
**Reason:** Apple removed the "Moments" view from Photos in iOS 13 (2019), replacing it with Days/Months/Years/All Photos, so the described navigation path no longer exists in the app; batch selection now works from any of those views anyway.
**Find this exact text in the doc:**
"""
And within Photos on iOS, batch-deleting images normally isn't possible outside of the Moments section, where whole Moments can be selected and deleted together rather than removing photos one at a time[^202].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2014 tip explained that batch-deleting photos in iOS was only possible from the Photos app's "Moments" section. Apple removed the Moments view in iOS 13 (2019), replacing it with Days/Months/Years/All Photos views, and batch selection/deletion now works from any of those views, not just one specific section. [^202]
"""

## [^203] PSA: Your Phone Logs Everywhere You Go. Here's How to Turn It Off
**Verdict:** SOFTEN
**Reason:** The general concept (both platforms track location) remains true, but this is a 2019 walkthrough and both Android and iOS have since added significantly more granular location controls (precise-location toggles, one-time permissions), so the specific menu paths have likely moved.
**Find this exact text in the doc:**
"""
Both Android and iPhone track a user's location continuously to support features like GPS, local search, and weather, and a walkthrough covered how to manage or opt out of that location-tracking behavior on each platform[^203].
"""
**Replace with:**
"""
Both Android and iPhone track a user's location to support features like GPS, local search, and weather, and a 2019 walkthrough covered how to manage or opt out of that location-tracking behavior on each platform — both platforms have since added finer-grained controls (like "precise location" toggles and one-time permissions), so it's worth checking the current Settings menus directly rather than following the exact steps from 2019[^203].
"""

## [^206] Everyday.me Is a Journaling App for iPhone That Writes Itself
**Verdict:** ARCHIVE
**Reason:** No current app store listing or working website could be found for Everyday.me; the small 2012-era startup app appears to be defunct.
**Find this exact text in the doc:**
"""
In a similar vein, the app Everyday.me automatically pulls in posts from a user's Twitter, Facebook, and Instagram accounts to build a running personal journal, which can also be supplemented by emailing entries directly to the app or adding them manually[^206].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- Everyday.me was a 2012 iPhone journaling app that automatically pulled in posts from a user's Twitter, Facebook, and Instagram accounts to build a running journal. The app no longer appears to be available or maintained. [^206]
"""

## [^207] Use Siri and IFTTT to Add Voice To-Dos to Astrid
**Verdict:** ARCHIVE
**Reason:** Astrid was acquired by Yahoo in May 2013 and its service was completely shut down that August, so the entire IFTTT-to-Astrid workflow described no longer has anything to route to.
**Find this exact text in the doc:**
"""
Voice assistants and connected gadgets rounded out the mobile category. Combining IFTTT with Siri allowed iOS users to add voice-dictated to-do items to the task manager Astrid by speaking a command to Siri, which emailed the to-do to Astrid for automatic routing into a to-do list[^207].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2012 tip described using IFTTT and Siri to add voice-dictated to-dos to the task manager Astrid by having Siri email the to-do for automatic routing into a to-do list. Astrid was acquired by Yahoo in May 2013 and its service was shut down that August, so the workflow is defunct. [^207]
"""

## [^209] Everything You Need to Know About USB 4
**Verdict:** SOFTEN
**Reason:** This 2020 explainer is framed around an upcoming standard; USB4 (and a later USB4 2.0 revision) has since become mainstream, so the "approaching" framing is stale even though the underlying background information is still reasonable.
**Find this exact text in the doc:**
"""
And as USB4 approached, a explainer rounded up what the new standard would mean for the many devices that rely on USB, comparing the moment to other looming standards like Wi-Fi 6E and mobile 5G[^209].
"""
**Replace with:**
"""
And as USB4 was first arriving, a 2020 explainer rounded up what the new standard would mean for the many devices that rely on USB, comparing the moment to other looming standards like Wi-Fi 6E and mobile 5G; USB4 (and its later USB4 2.0 revision) is now widely shipped, so the piece is useful mainly as background on the standard rather than a preview of what's coming[^209].
"""

## [^210] Facebook Auto-Sharing Apps Get a Little Less Creepy, But You Should Still Avoid Them
**Verdict:** ARCHIVE
**Reason:** Both named examples are dead — Socialcam was discontinued by Autodesk in 2015, and The Washington Post's Social Reader was pulled not long after this piece ran — and Facebook has since sharply scaled back the automatic-share News Feed integrations ("frictionless sharing"/Open Graph actions) these apps depended on.
**Find this exact text in the doc:**
"""
So-called "frictionless sharing" apps, such as Socialcam or The Washington Post's Social Reader, automatically posted what a friend watched or read to their news feed—often without the friend realizing it—and even after Facebook introduced new rules to curb accidental auto-sharing, the practice remained worth avoiding[^210].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2012 warning about Facebook "frictionless sharing" apps singled out Socialcam and The Washington Post's Social Reader as examples that auto-posted activity to friends' news feeds. Socialcam was discontinued by Autodesk in 2015, the Social Reader was pulled not long after this piece ran, and Facebook has since scaled back the automatic-share app integrations both relied on. [^210]
"""

## [^211] Put "Congratulations" in Your Facebook Post So More People See It
**Verdict:** ARCHIVE
**Reason:** This isn't just dated — Facebook has explicitly targeted this exact category of "engagement bait" (comment/react/share baiting) with algorithmic demotion since December 2017, so following the old advice today is more likely to hurt a post's reach than help it.
**Find this exact text in the doc:**
"""
Separately, one theory held that including the word "congratulations" in a Facebook post could cause the platform's news-feed algorithm to push that post higher in friends' feeds, since users are inclined to click through and offer their own congratulations[^211].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2014 item repeated a theory that including the word "congratulations" in a Facebook post could boost its News Feed ranking by prompting replies. Facebook has since explicitly classified this kind of tactic as "engagement bait" and begun algorithmically demoting posts that use it (starting December 2017), so following this advice today is more likely to hurt a post's reach than help it. [^211]
"""

## [^218] Import.io Turns Web Pages Into a Useable Data Table
**Verdict:** ARCHIVE
**Reason:** Import.io has discontinued the free, click-a-button consumer desktop app described in this tip and repositioned entirely as a paid enterprise web-scraping platform starting around $199/month, so the original casual-user workflow no longer exists.
**Find this exact text in the doc:**
"""
Import.io lets Windows, OS X, and Linux users pull data directly from a web page's underlying code into a usable table just by navigating to that page inside the app and clicking a button, cutting out the need to enter each piece of information by hand[^218].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2014 tip recommended Import.io's free desktop app for pulling data from a web page into a table with a click. Import.io has since discontinued that free consumer app and repositioned itself as a paid enterprise web-scraping platform starting around $199/month, so the tip's original free, casual-user workflow no longer exists. [^218]
"""

## [^220] KeepItWith.Me Offers Dead Simple URL Sharing Between Devices
**Verdict:** ARCHIVE
**Reason:** The site currently returns a server error (unreachable origin) and shows no sign of active operation; the tip's entire value depended on this now-defunct 2010-era service.
**Find this exact text in the doc:**
"""
And for the simple task of shuttling a single link between devices or browsers, KeepItWith.Me offered a one-click system for sharing URLs, in contrast to earlier, more restrictive tools like Chrome to Phone or GMailThis[^220].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2010 tip highlighted KeepItWith.Me, a one-click tool for sharing a URL between devices or browsers. The site no longer loads (it returns a server error), and modern OS-level features like iCloud Handoff and cross-device browser sync have largely replaced the need it served. [^220]
"""

## [^224] Send Your Kindle Book Notes and Highlighted Passages to Evernote
**Verdict:** SOFTEN
**Reason:** Amazon's Kindle notes/highlights page and the Evernote web clipper workflow both still work, but Evernote's 2023 acquisition by Bending Spoons cut its free plan down to just 50 notes in one notebook, undermining the "single searchable archive" premise for readers without a paid plan.
**Find this exact text in the doc:**
"""
And Kindle readers who highlight and annotate books can send those notes and highlighted passages into Evernote using the Evernote web clipper on the notes-and-highlights page of their Amazon Kindle account, creating a single searchable archive of book quotes[^224].
"""
**Replace with:**
"""
And Kindle readers who highlight and annotate books can send those notes and highlighted passages into Evernote using the Evernote web clipper on the notes-and-highlights page of their Amazon Kindle account, creating a searchable archive of book quotes — though Evernote's free plan has since been cut down to just 50 notes in a single notebook under its current ownership, so heavy Kindle-highlight archiving now generally requires a paid plan or an alternative tool like Clippings.io[^224].
"""

## [^229] Learn Linux with This Free edX Course from the Linux Foundation
**Verdict:** SOFTEN
**Reason:** The Linux Foundation's Intro to Linux course is still offered as a free audit on edX, but the "$2,400 course" framing and certificate pricing are outdated, and edX's parent company (2U) filed for bankruptcy in 2024, so both the price and the platform's stability have changed since this 2014 article.
**Find this exact text in the doc:**
"""
On the operating-system side, the Linux Foundation's normally $2,400 "Intro to Linux" course was offered for free through edX, with a recommendation to install Linux ahead of the course's start date to get the most out of it[^229].
"""
**Replace with:**
"""
On the operating-system side, the Linux Foundation's "Intro to Linux" course (LFS101) has long been offered as a free audit course through edX, with a paid certificate option for those who want one, and a recommendation to install Linux ahead of time to get the most out of it — note that edX's ownership and pricing have changed since this 2014 article (edX's parent company, 2U, filed for bankruptcy in 2024), so it's worth checking current pricing and platform status before enrolling[^229].
"""

## [^230] See All of Google's Computer Science Education Tools and Programs in One Place
**Verdict:** ARCHIVE
**Reason:** Google shut down CS First — one of the two flagship programs named — on June 30, 2025 (pointing schools instead to the Raspberry Pi Foundation's Experience CS), so the described consolidated resource page no longer reflects Google's current CS education offerings.
**Find this exact text in the doc:**
"""
Google separately consolidated its computer-science education efforts—including the girls-focused Made with Code initiative and the CS First computer-science clubs program—into a single site covering scholarships, academic opportunities, and other programs for students and kids[^230].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2016 item pointed to a Google site consolidating its computer-science education programs, including the girls-focused Made with Code initiative and the CS First computer-science clubs program. Google shut down CS First on June 30, 2025 (pointing schools instead to the Raspberry Pi Foundation's Experience CS), so this consolidated resource page no longer reflects Google's current CS education offerings. [^230]
"""

## [^234] What to Do If You Can't Pay Your Phone Bill Right Now
**Verdict:** ARCHIVE
**Reason:** The FCC's Keep Americans Connected Pledge was a time-limited COVID-19-era program that expired June 30, 2020 and was never renewed, so it's no longer an available option.
**Find this exact text in the doc:**
"""
On the financial side of the pandemic's shift to remote everything, heavier cell phone usage while spending more time at home prompted a look at options for people who couldn't pay their phone bill, including the FCC's "Keep Americans Connected Pledge," which more than 700 companies signed on to in order to maintain customers' phone and internet service for a period of time[^234].
"""
**Archive entry (ready to paste under a `### <subheading>` in the Archive section):**
"""
- A 2020 item covered options for paying a phone bill during pandemic-related financial strain, including the FCC's "Keep Americans Connected Pledge," which more than 700 companies signed on to. That pledge was a time-limited program that expired on June 30, 2020, and was not extended, so it is no longer available. [^234]
"""
