-- Blue Vomit research session 10 - 2026-09-19

INSERT INTO core_link (band_id, link_type, title, url, description, is_primary, created_at) VALUES
(70, 'purchase', 'F.O.A.D. Records — Blue Vomit Discografia 1982/83', 'https://www.foadrecords.com/index.php/blue-vomit-discografia-1982-83-out-now/', 'F.O.A.D. Records LP reissue', false, NOW()),
(70, 'purchase', 'Hells Headbangers — Blue Vomit LP', 'https://shop-hellsheadbangers.com/blue-vomit-discografia-1982-83-LP.asp', 'Hells Headbangers LP', false, NOW()),
(70, 'purchase', 'Puke N Vomit Records — Blue Vomit LP', 'https://pukenvomitrecords.com/products/blue-vomit-discografia-198x-new-lp', 'Puke N Vomit Records LP', false, NOW()),
(70, 'purchase', 'Velted Regnub Mailorder — Blue Vomit LP (black)', 'https://veltedregnubmailorder.bigcartel.com/product/blue-vomit-discografia-198x-lp-black', 'Velted Regnub Mailorder LP (black vinyl)', false, NOW()),
(70, 'archive', 'Punkadeka — Blue Vomit', 'https://www.punkadeka.it/blue-vomit/', 'Punk web magazine', false, NOW()),
(70, 'archive', 'DeBaser — Blue Vomit Demo 83', 'https://en.debaser.it/blue-vomit', 'DeBaser review', false, NOW()),
(70, 'archive', 'Last.fm — Blue Vomit', 'https://www.last.fm/music/Blue+Vomit', 'Last.fm artist page', false, NOW()),
(70, 'archive', 'Internet Archive — Torino 198X', 'https://archive.org/details/youtube-UBrivRoG5GM', 'Internet Archive compilation tape', false, NOW()),
(70, 'archive', 'Anarcho-punk.net — Blue Vomit', 'https://anarcho-punk.net/band?band=Blue%20Vomit', 'Anarcho-punk.net band page', false, NOW()),
(70, 'archive', 'Discogs — Vivo In Una Città Morta (2012)', 'https://www.discogs.com/release/13407397-Blue-Vomit-Vivo-In-Una-Città-Morta', 'Discogs release', false, NOW()),
(70, 'archive', 'Italian Wikipedia — Hardcore punk italiano', 'https://it.wikipedia.org/wiki/Hardcore_punk_italiano', 'Wikipedia article', false, NOW()),
(70, 'video', 'YouTube — Blue Vomit Discografia 198X (Full LP)', 'https://www.youtube.com/watch?v=TrNjR0nfrtQ', 'Full LP YouTube video', false, NOW()),
(70, 'video', 'YouTube — Blue Vomit Vivo In Una Città Morta', 'https://www.youtube.com/watch?v=EzZUoL4zmEg', 'YouTube video', false, NOW()),
(70, 'video', 'YouTube — Blue Vomit Vivo In Una Città Morta (2012 Remaster)', 'https://www.youtube.com/watch?v=jczm8YUddqg', '2012 remastered version', false, NOW()),
(70, 'archive', 'Lyrics Translate — Blue Vomit', 'https://lyricstranslate.com/en/blue-vomit-vivo-una-citta-morta-lyrics.html', 'Lyrics + translations', false, NOW()),
(70, 'archive', 'Kleisma — Enrico Falulera (drummer)', 'https://www.kleisma.com/musicisti/profilo/enrico-falulera', 'Drummer bio', false, NOW());

-- Add connections with source AND notes (both NOT NULL)
INSERT INTO core_bandconnection (from_band_id, to_band_id, connection_type, source, notes, created_at)
SELECT 70, 71, 'shared_member', 'Purple Hat Research', 'Luca Abort (vocals) and Simone Cinotto (guitar) went from Blue Vomit to Nerorgasmo', NOW()
WHERE NOT EXISTS (SELECT 1 FROM core_bandconnection WHERE from_band_id=70 AND to_band_id=71);

INSERT INTO core_bandconnection (from_band_id, to_band_id, connection_type, source, notes, created_at)
SELECT 70, 72, 'shared_member', 'Purple Hat Research', 'Some Blue Vomit members went to Declino', NOW()
WHERE NOT EXISTS (SELECT 1 FROM core_bandconnection WHERE from_band_id=70 AND to_band_id=72);

INSERT INTO core_bandconnection (from_band_id, to_band_id, connection_type, source, notes, created_at)
SELECT 70, 64, 'scene_peer', 'Purple Hat Research', 'Torino punk scene', NOW()
WHERE NOT EXISTS (SELECT 1 FROM core_bandconnection WHERE from_band_id=70 AND to_band_id=64);

-- Verify
SELECT '=== Links for Blue Vomit: ===' as info;
SELECT id, link_type, title FROM core_link WHERE band_id=70 ORDER BY id DESC LIMIT 25;
SELECT '=== Connections for Blue Vomit: ===' as info;
SELECT id, from_band_id, to_band_id, connection_type, notes FROM core_bandconnection WHERE from_band_id=70 OR to_band_id=70;
