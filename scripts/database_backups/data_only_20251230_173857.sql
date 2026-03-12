--
-- PostgreSQL database dump
--

\restrict o0wGLEVhv1BR3wyuIYPpUJsgN4PxsBrb4sc207A7reDLRpCBuujk59fM6nxqpf3

-- Dumped from database version 13.22 (Debian 13.22-1.pgdg13+1)
-- Dumped by pg_dump version 13.22 (Debian 13.22-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
4c1e0f46831c
add_files_table
\.


--
-- Data for Name: contributors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contributors (id, name, email, role, bio, profile_image, github_url, linkedin_url, website_url, created_at, updated_at) FROM stdin;
019b25b8-3071-7185-91e3-590b8dba5156	Wempy Wiryawan	adityaw@example.com	UI/UX Designer	Creative designer with passion for user experience		https://github.com/alice	https://linkedin.com/in/alice	https://alice-portfolio.com	2025-12-16 05:53:06.673469+00	2025-12-20 01:52:06.202442+00
019b25b4-9d33-745a-a3a5-97da6a7f3839	Alice Johnsonn	alice@example.com	Full Stack Developer	Updated bio: Senior Full Stack Developer with 7+ years experience		https://github.com/alice	https://linkedin.com/in/alice	https://alice-portfolio.com	2025-12-16 05:49:12.371813+00	2025-12-20 01:53:58.406286+00
019b25b6-557d-7e4e-b1ec-9e4411b788b9	Alice Johnsom	alice@example.com	Full Stack Developer	Updated bio: Senior Full Stack Developer with 7+ years experience		https://github.com/alice	https://linkedin.com/in/alice	https://alice-portfolio.com	2025-12-16 05:51:05.08535+00	2025-12-20 01:56:21.729212+00
019b25b8-30a5-7eea-843b-06feb60c57c3	Bob Smithh	bob@example.com	Data Scientist	ML engineer specializing in computer vision		https://github.com/bob		https://wempy.com	2025-12-16 05:53:06.725736+00	2025-12-20 02:16:09.863538+00
\.


--
-- Data for Name: dataset_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dataset_categories (id, name, slug, description, created_at) FROM stdin;
f4354936-e560-4c05-8778-ab7b963255f4	Computer Vision	computer-vision	Datasets for computer vision tasks	2025-12-03 14:44:29.896551+00
3d4ca45d-dd2a-4a8e-8e18-d677031f5375	Natural Language Processing	nlp	Datasets for NLP tasks	2025-12-03 14:44:29.896551+00
019ae7a5-e7ec-79ec-9eca-b0c0939c3073	Deep learning asas	deep-learning-asas	Category for deep learning related content	2025-12-04 04:36:41.068992+00
019aecfd-17ed-78e3-a46d-8ce0f8ce46a0	Deep learning dataset	deep-learning-dataset	Category for deep learning related content	2025-12-05 05:30:01.069236+00
\.


--
-- Data for Name: tier; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tier (id, name, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password_hash, role, is_active, is_deleted, created_at, updated_at, username, profile_image_url, deleted_at, is_superuser, tier_id) FROM stdin;
019aabe5-142c-747d-8571-ee9cf89ae01a	Test User	test@example.com	$2b$12$hashedpassword	registered	t	f	2025-11-22 14:13:05.080505+00	\N	\N	\N	\N	f	\N
019aac00-a7e2-7436-bec3-c642320947c7	New User	newuser@example.com	$2b$12$oRMvg31KLiJE0y1rYtaCBe690CPlGE4GPtZrwfU27ZgcECHBd4GsK	registered	t	f	2025-11-22 14:38:35.490692+00	\N	\N	\N	\N	f	\N
019aac01-9dae-74ec-bff8-02dc9ebb64d0	Brand New User	brandnew@example.com	$2b$12$zy2RtRB.mCxkjjEr4zBjiOSb0RzZEoTEcNmKHfh0AFlzqmRNj5s42	registered	t	f	2025-11-22 14:39:38.414454+00	\N	\N	\N	\N	f	\N
019aac02-ac77-7338-ac5b-3a8446f4a76d	Super New User	supernew@example.com	$2b$12$uC9OZciCtwx3h.9pjgpFTeL/EmuATB19YQf0.W4j.eEfmmRc/5wdm	admin	t	f	2025-11-22 14:40:47.736042+00	\N	\N	\N	\N	t	\N
019aabfc-de4c-7653-b8e1-4410ccec2c33	Admin User	admin@example.com	$2b$12$Yzk8537szIIuBYH24SPVZeFJ2ErTIvu48.ROFlALoclGuupbBO.Zm	admin	t	f	2025-11-22 14:34:27.277006+00	2025-12-10 10:36:07.248531+00	admin	\N	\N	t	\N
\.


--
-- Data for Name: datasets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datasets (id, name, slug, description, sample_image_url, file_url, source, size, access_level, status, created_by, created_at, updated_at, tagline, samples, download_count, gradient, version, format, license, citation, key_features, use_cases, technical_specs, statistics, sample_images, view_count) FROM stdin;
019ae4aa-c9e7-7bc2-a541-f6b7bcc9e7f5	DATASET INI MAH HAHAHA	dataset-ini-mah-hahaha	A comprehensive dataset for advanced computer vision research	\N	https://example.com/advanced_cv_dataset.zip	Advanced Research Lab	2048000000	public	published	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-03 14:43:09.415506+00	2025-12-29 03:34:47.3573+00	Updated: Premium computer vision dataset	60000	0	#FF6B6B,#4ECDC4	2.2	JSON	MIT	@dataset{adv_cv_2024, author={Research Team}, title={Advanced CV Dataset}}	{"Ultra high resolution","Real-time annotations","Multi-modal data"}	{"Object detection","Image classification","Computer vision research","Deep learning"}	{"type": "supervised", "access": "public", "format": "JSON", "license": "MIT", "version": "2.1", "lastUpdate": "2024-01-15"}	{"avgImageSize": "1024x1024", "qualityScore": 9.8, "totalAnnotations": 60000, "avgImagesPerCategory": 6000, "maxImagesPerCategory": 6500, "minImagesPerCategory": 5500}	{https://picsum.photos/200/300?random=1,https://picsum.photos/200/300?random=2,https://picsum.photos/200/300?random=3,https://picsum.photos/200/300?random=4}	2
019ae4b2-d4c7-7a18-890d-80db7143746a	Advanced Computer Vision Dataset 2	advanced-cv-dataset-2	A comprehensive dataset for advanced computer vision research	\N	https://example.com/advanced_cv_dataset.zip	Advanced Research Lab	2048000000	public	published	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-03 14:51:56.4876+00	2025-12-12 09:35:47.932873+00	State-of-the-art computer vision training data	50000	6	#FF6B6B,#4ECDC4	2.1	JSON	MIT	@dataset{adv_cv_2024, author={Research Team}, title={Advanced CV Dataset}}	{"High resolution images","Balanced classes","Quality annotations","Diverse scenarios"}	{"Object detection","Image classification","Computer vision research","Deep learning"}	{"type": "supervised", "access": "public", "format": "JSON", "license": "MIT", "version": "2.1", "lastUpdate": "2024-01-15"}	{"avgImageSize": "512x512", "qualityScore": 9.5, "totalAnnotations": 50000, "avgImagesPerCategory": 5000, "maxImagesPerCategory": 5500, "minImagesPerCategory": 4500}	{https://example.com/sample1.jpg,https://example.com/sample2.jpg,https://example.com/sample3.jpg}	15
\.


--
-- Data for Name: dataset_category_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dataset_category_links (id, dataset_id, category_id, created_at) FROM stdin;
019ae4bb-5a5c-70fe-b9ea-82dc609ba495	019ae4aa-c9e7-7bc2-a541-f6b7bcc9e7f5	f4354936-e560-4c05-8778-ab7b963255f4	2025-12-03 15:01:14.972512+00
019b02ea-f233-7ec6-94fe-5cab5484a460	019ae4b2-d4c7-7a18-890d-80db7143746a	f4354936-e560-4c05-8778-ab7b963255f4	2025-12-09 11:41:50.515682+00
019b02ea-f236-7a6c-bc1f-2e1aa4b30890	019ae4b2-d4c7-7a18-890d-80db7143746a	3d4ca45d-dd2a-4a8e-8e18-d677031f5375	2025-12-09 11:41:50.518694+00
\.


--
-- Data for Name: dataset_contributor_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dataset_contributor_links (id, dataset_id, contributor_id, role_in_dataset, created_at) FROM stdin;
\.


--
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.files (id, original_filename, filename, file_path, file_url, file_type, mime_type, file_size, uploaded_by, file_metadata, description, created_at, updated_at) FROM stdin;
019b2ac3-672b-71e6-86db-58d8cd78d988	avatar-15.png	avatar-15_20251217_052327_657848.png	2025/12/avatar-15_20251217_052327_657848.png	/uploads/2025/12/avatar-15_20251217_052327_657848.png	image	image/png	5605	019aac02-ac77-7338-ac5b-3a8446f4a76d	\N	\N	2025-12-17 05:23:27.659811+00	\N
019b2c26-415d-7538-bfd6-b5b99c539b1f	000000002006.jpg	000000002006_20251217_115103_251339.jpg	2025/12/000000002006_20251217_115103_251339.jpg	/uploads/2025/12/000000002006_20251217_115103_251339.jpg	image	image/jpeg	202589	019aac02-ac77-7338-ac5b-3a8446f4a76d	\N	\N	2025-12-17 11:51:03.261286+00	\N
019b3969-cb88-7eb5-bf38-fb144231bd5e	000000000285.jpg	000000000285_20251220_013953_344740.jpg	2025/12/000000000285_20251220_013953_344740.jpg	/uploads/2025/12/000000000285_20251220_013953_344740.jpg	image	image/jpeg	335861	019aac02-ac77-7338-ac5b-3a8446f4a76d	\N	\N	2025-12-20 01:39:53.353258+00	\N
019b397a-e653-7e0f-b421-3f107e3edd86	000000000724.jpg	000000000724_20251220_015834_321854.jpg	2025/12/000000000724_20251220_015834_321854.jpg	/uploads/2025/12/000000000724_20251220_015834_321854.jpg	image	image/jpeg	130107	019aac02-ac77-7338-ac5b-3a8446f4a76d	\N	\N	2025-12-20 01:58:34.323715+00	\N
019b6ddf-ee5f-7224-ad1e-bb769cc98ffc	ex_error.png	ex_error_20251230_060910_745192.png	2025/12/ex_error_20251230_060910_745192.png	/uploads/2025/12/ex_error_20251230_060910_745192.png	image	image/png	29435	019aac02-ac77-7338-ac5b-3a8446f4a76d	\N	\N	2025-12-30 06:09:10.751603+00	\N
\.


--
-- Data for Name: models; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.models (id, name, slug, description, architecture, dataset_used, metrics, model_file_url, access_level, status, created_by, created_at, updated_at) FROM stdin;
019b06f7-7eda-756f-8755-9401a8d25b6c	Flexible Metrics Test	flex-test-1765348441	Testing	Test	\N	{"fid": 12.5, "map": 0.78, "accuracy": 0.95, "precision": 0.93, "custom_value": "test"}	\N	public	draft	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-10 06:34:01.818479+00	\N
019b06f7-e67c-706d-b504-ec17af1dc2e2	Complete Metrics Test	complete-metrics-1765348468	All metric types	Multi	\N	{"fid": 12.5, "iou": 0.82, "mae": 0.15, "map": 0.78, "mse": 0.023, "bleu": 0.45, "rmse": 0.152, "map_50": 0.85, "recall": 0.94, "accuracy": 0.95, "f1_score": 0.92, "r2_score": 0.89, "precision": 0.93, "custom_metric": "any value", "gpu_memory_gb": 8, "model_size_mb": 250, "inception_score": 8.3, "inference_time_ms": 45, "training_time_hours": 2.5}	https://spmb1.wempyaw.com/uploads/2025/12/000000002006_20251217_115103_251339.jpg	public	published	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-10 06:34:28.348544+00	2025-12-20 07:19:45.113908+00
019ac109-2883-71ab-b29c-16488d7c2278	ResNet-50 Image Classifier	resnet-50-image-classifier	A deep residual network for image classification	ResNet	ImageNet	{"MAE": 100, "loss": 0.05, "accuracy": 0.95, "f1_score": 0.92}	https://spmb1.wempyaw.com/uploads/2025/12/avatar-15_20251217_052327_657848.png	public	draft	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-11-26 16:39:54.243311+00	2025-12-20 07:20:03.223543+00
\.


--
-- Data for Name: gallery; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gallery (id, prompt, image_url, extra_metadata, model_id, created_by, created_at, updated_at) FROM stdin;
019b14df-e591-755e-9dc8-efb6324dd3ed	Static Random Image	https://picsum.photos/720/480?random=2	null	\N	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-12 23:22:56.273366+00	2025-12-12 23:27:07.479954+00
019b14e2-b519-79ce-a099-a67542dbe0f3	RANDOM IMAGE 2	https://picsum.photos/720/480?random=3	null	\N	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-12 23:26:00.473916+00	2025-12-12 23:27:21.435934+00
019b14e3-33da-76fc-873d-1d1ccb141414	RANDOM IMAGE 4	https://picsum.photos/720/480?random=4	null	\N	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-12 23:26:32.92254+00	2025-12-12 23:27:32.674262+00
019b14e2-f37c-7b41-bc98-d91fe23c9a36	RANDOM IMAGE 3	https://picsum.photos/720/480?random=5	null	\N	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-12 23:26:16.444425+00	2025-12-12 23:27:44.178697+00
019ac4dd-f912-7aad-b35a-cce0bf96f342	Beautiful mountain landscape	https://picsum.photos/720/480?random=6	null	\N	019aabfc-de4c-7653-b8e1-4410ccec2c33	2025-11-27 10:31:12.914377+00	2025-12-12 23:27:51.177306+00
019b391f-4064-7075-949a-a9b08f5d36ff	user avatar	https://spmb1.wempyaw.com/uploads/2025/12/000000002006_20251217_115103_251339.jpg	null	\N	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-20 00:18:28.068356+00	2025-12-20 00:18:37.103249+00
019b14e2-8cf8-7873-a6d4-742f1ed3271b	RANDOM IMAGE 1	https://spmb1.wempyaw.com/uploads/2025/12/000000000285_20251220_013953_344740.jpg	null	\N	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-12 23:25:50.200651+00	2025-12-20 07:26:14.383373+00
\.


--
-- Data for Name: gallery_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gallery_categories (id, name, slug, description, created_at) FROM stdin;
019ac4cd-1e4b-7a00-ba69-bfaaa1488a56	Digital Art	digital-art	AI generated digital artwork	2025-11-27 10:12:48.331343+00
019b06ce-a9fc-7134-b79e-cecdfc511e8e	Deep learning gallery	deep-learning-gallery	Category for deep learning related content	2025-12-10 05:49:25.88491+00
\.


--
-- Data for Name: gallery_category_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gallery_category_links (id, gallery_id, category_id, created_at) FROM stdin;
019b06dd-7ae3-7a9b-aa91-b9e1272baeae	019ac4dd-f912-7aad-b35a-cce0bf96f342	019b06ce-a9fc-7134-b79e-cecdfc511e8e	2025-12-10 06:05:36.867485+00
\.


--
-- Data for Name: model_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.model_categories (id, name, slug, description, created_at) FROM stdin;
019ac0fd-ec13-7b13-845b-1965c26ac93a	Computer Vision	computer-vision	AI models for image and video processing	2025-11-26 16:27:37.875579+00
\.


--
-- Data for Name: model_category_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.model_category_links (id, model_id, category_id, created_at) FROM stdin;
019aee0b-c8ae-7f46-b8b8-5bd97814f03d	019ac109-2883-71ab-b29c-16488d7c2278	019ac0fd-ec13-7b13-845b-1965c26ac93a	2025-12-05 10:25:41.038495+00
\.


--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news (id, title, slug, content, thumbnail_url, tags, access_level, status, created_by, created_at, updated_at) FROM stdin;
019b154d-0346-7ad0-8f5f-1c061fb6d483	ini adalah berita baru	ini-adalah-berita-baru	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam finibus mattis eros, ac tempor tellus venenatis eu. Fusce quis placerat diam. Quisque at dignissim ipsum. Pellentesque sodales risus in malesuada eleifend. Nam semper interdum pharetra. Sed lobortis sit amet massa sed pharetra. Maecenas fermentum nunc non massa vehicula, at mollis augue rutrum. Duis cursus eros non porttitor malesuada.\n\nMaecenas a finibus ipsum. Maecenas rhoncus tincidunt tincidunt. Integer ut convallis lorem. Proin ornare semper tincidunt. Aenean rhoncus eget enim nec dignissim. Nam elementum nec augue sit amet accumsan. Proin aliquet libero ex, sit amet feugiat neque varius quis. Ut volutpat purus vel egestas interdum. Suspendisse pharetra accumsan mi. Praesent fermentum, justo et rutrum semper, turpis arcu cursus odio, et tempus leo nisi non est. Praesent urna neque, luctus non molestie rutrum, fermentum id neque. Sed facilisis quis metus et tincidunt. Praesent non vulputate erat.\n\nInteger dignissim malesuada blandit. Vestibulum risus nisi, gravida in nisi quis, sagittis pellentesque dolor. Nullam egestas lorem ut lectus suscipit vulputate eget et velit. Aliquam vitae sollicitudin nisl. Fusce sollicitudin justo non nibh viverra, ut lacinia dolor dignissim. Cras rhoncus eleifend eros at ultrices. Duis at tortor vel lorem congue cursus a in sem. Praesent tortor orci, semper sit amet egestas sit amet, accumsan nec nulla. Aliquam erat volutpat. Nulla facilisi.\n\nClass aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas enim mauris, lobortis nec sem rutrum, mollis posuere justo. Quisque vel ante sit amet ante finibus vehicula sed at mi. Nam eget tellus non leo porttitor cursus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque in ante ipsum. Nullam magna justo, cursus id augue ac, pulvinar molestie lorem. Vivamus vitae malesuada eros. Praesent rhoncus dui a pulvinar feugiat. Aliquam vel augue nisi. Praesent nec neque suscipit, lobortis leo ac, malesuada sapien. Curabitur faucibus auctor lectus eget placerat. Phasellus sit amet luctus lorem. Aenean malesuada ullamcorper nisi nec varius. Aenean rhoncus ex et volutpat ultricies. Ut efficitur metus vitae leo posuere, tincidunt sodales quam porttitor.\n\nQuisque cursus at ante ut scelerisque. Etiam vitae nisi ac leo gravida tincidunt at id est. Suspendisse a euismod velit. Pellentesque et rutrum nisl. Phasellus hendrerit tempus turpis, in pulvinar nulla. Mauris eu accumsan nibh. Morbi risus eros, blandit in enim non, fermentum pharetra neque. Curabitur non malesuada ex, ac blandit ipsum. Maecenas eu nulla dolor. Morbi consectetur faucibus justo, id dignissim augue pulvinar sodales. Proin vestibulum felis quis mattis varius. In hac habitasse platea dictumst. Nulla vel malesuada eros. Proin eu dapibus nisl.	https://spmb1.wempyaw.com/uploads/2025/12/000000000724_20251220_015834_321854.jpg	{a,b,c,d}	public	published	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-13 01:22:07.302875+00	2025-12-20 02:16:33.987742+00
019abdfd-d849-7f0f-8f98-aa9c71342a90	Breaking: New AI Breakthroughh	new-ai-breakthroughh	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam finibus mattis eros, ac tempor tellus venenatis eu. Fusce quis placerat diam. Quisque at dignissim ipsum. Pellentesque sodales risus in malesuada eleifend. Nam semper interdum pharetra. Sed lobortis sit amet massa sed pharetra. Maecenas fermentum nunc non massa vehicula, at mollis augue rutrum. Duis cursus eros non porttitor malesuada.\n\nMaecenas a finibus ipsum. Maecenas rhoncus tincidunt tincidunt. Integer ut convallis lorem. Proin ornare semper tincidunt. Aenean rhoncus eget enim nec dignissim. Nam elementum nec augue sit amet accumsan. Proin aliquet libero ex, sit amet feugiat neque varius quis. Ut volutpat purus vel egestas interdum. Suspendisse pharetra accumsan mi. Praesent fermentum, justo et rutrum semper, turpis arcu cursus odio, et tempus leo nisi non est. Praesent urna neque, luctus non molestie rutrum, fermentum id neque. Sed facilisis quis metus et tincidunt. Praesent non vulputate erat.\n\nInteger dignissim malesuada blandit. Vestibulum risus nisi, gravida in nisi quis, sagittis pellentesque dolor. Nullam egestas lorem ut lectus suscipit vulputate eget et velit. Aliquam vitae sollicitudin nisl. Fusce sollicitudin justo non nibh viverra, ut lacinia dolor dignissim. Cras rhoncus eleifend eros at ultrices. Duis at tortor vel lorem congue cursus a in sem. Praesent tortor orci, semper sit amet egestas sit amet, accumsan nec nulla. Aliquam erat volutpat. Nulla facilisi.\n\nClass aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas enim mauris, lobortis nec sem rutrum, mollis posuere justo. Quisque vel ante sit amet ante finibus vehicula sed at mi. Nam eget tellus non leo porttitor cursus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque in ante ipsum. Nullam magna justo, cursus id augue ac, pulvinar molestie lorem. Vivamus vitae malesuada eros. Praesent rhoncus dui a pulvinar feugiat. Aliquam vel augue nisi. Praesent nec neque suscipit, lobortis leo ac, malesuada sapien. Curabitur faucibus auctor lectus eget placerat. Phasellus sit amet luctus lorem. Aenean malesuada ullamcorper nisi nec varius. Aenean rhoncus ex et volutpat ultricies. Ut efficitur metus vitae leo posuere, tincidunt sodales quam porttitor.\n\nQuisque cursus at ante ut scelerisque. Etiam vitae nisi ac leo gravida tincidunt at id est. Suspendisse a euismod velit. Pellentesque et rutrum nisl. Phasellus hendrerit tempus turpis, in pulvinar nulla. Mauris eu accumsan nibh. Morbi risus eros, blandit in enim non, fermentum pharetra neque. Curabitur non malesuada ex, ac blandit ipsum. Maecenas eu nulla dolor. Morbi consectetur faucibus justo, id dignissim augue pulvinar sodales. Proin vestibulum felis quis mattis varius. In hac habitasse platea dictumst. Nulla vel malesuada eros. Proin eu dapibus nisl.	https://picsum.photos/200/300?random=1	{ai,breakthrough,technology,updated,ml}	public	published	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-11-26 02:28:41.161916+00	2025-12-13 02:34:41.490981+00
\.


--
-- Data for Name: news_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news_categories (id, name, slug, description, created_at) FROM stdin;
019abe20-aab9-74f1-b17f-6286d6ddebf1	Technology	technology	Technology related news and updates	2025-11-26 03:06:43.257488+00
019abe20-de75-7b1b-85d6-6856bd6c2991	AI & Machine Learning	ai-machine-learning	Artificial Intelligence and Machine Learning news	2025-11-26 03:06:56.502032+00
019ac046-d8d1-7c75-973f-aaa6733e93d0	Technology News	technology-news	Latest technology updates and breakthroughs	2025-11-26 13:07:39.858167+00
019ac047-1b1d-7b57-8e4c-91f85d5dad2d	AI Research	ai-research	Artificial Intelligence research and development news	2025-11-26 13:07:56.831056+00
\.


--
-- Data for Name: news_category_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news_category_links (id, news_id, category_id, created_at) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, name, username, email, hashed_password, profile_image_url, uuid, created_at, updated_at, deleted_at, is_deleted, is_superuser, tier_id) FROM stdin;
\.


--
-- Data for Name: post; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.post (id, created_by_user_id, title, text, uuid, media_url, created_at, updated_at, deleted_at, is_deleted) FROM stdin;
\.


--
-- Data for Name: project_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_categories (id, name, slug, description, created_at) FROM stdin;
019aabe5-142c-747d-8571-ee9cf89ae01a	Machine Learning	machine-learning	Machine learning related projects	2025-11-22 14:08:28.204923+00
019aabe5-5991-7c7e-bf1a-5c2d41ad31a1	Web Development	web-development	Web applications and APIs	2025-11-22 14:08:45.969913+00
019aabe5-7647-75d1-9d2b-58a9fc0b35b8	Data Science	data-science	Data analysis and visualization	2025-11-22 14:08:53.319602+00
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, title, slug, description, thumbnail_url, tags, access_level, status, created_by, created_at, updated_at, full_description, technologies, challenges, achievements, future_work, complexity, start_at, demo_url) FROM stdin;
019ae400-8f72-7381-b71c-3a30aab2a55b	Advanced AI Batik Recognition	advanced-ai-batik-recognition	Short description of batik recognition project	https://picsum.photos/720/480?random=9	{AI,Culture,"Computer Vision"}	public	published	019aabe5-142c-747d-8571-ee9cf89ae01a	2025-12-03 11:37:13.330235+00	2025-12-29 00:33:39.788748+00	This is a comprehensive AI project that uses deep learning to recognize and classify different batik patterns from Indonesian traditional textiles. The project aims to preserve cultural heritage through technology.	{Python,TensorFlow,OpenCV,FastAPI,PostgreSQL}	{"Dataset collection","Pattern complexity","Color variations"}	{"95% accuracy","Real-time processing","Mobile app integration"}	{"Expand dataset","3D pattern recognition","Cultural documentation"}	hard	2024-01-01 00:00:00+00	{}
019ae40f-c036-75c8-95f9-1cfdde24aea1	Advanced AI Batik Recognition 4	advanced-ai-batik-recognition-4	Short description of batik recognition project	https://picsum.photos/720/480?random=8	{AI,Culture,"Computer Vision"}	public	published	019aabe5-142c-747d-8571-ee9cf89ae01a	2025-12-03 11:53:48.855059+00	2025-12-29 10:41:01.5487+00	This is a comprehensive description of our AI project with detailed explanations 2 4.	{Python,TensorFlow,Docker,FastAPI}	{"Data quality issues","Model optimization","Scalability concerns"}	{"90% accuracy achieved","Real-time inference implemented"}	{"Mobile app integration","Advanced analytics dashboard"}	medium	2024-01-15 00:00:00+00	{https://single-demo.example.com}
019afd30-2d9c-78de-a48b-10c172214c9d	Advanced AI Batik Recognition 3	advanced-ai-batik-recognition-3	Short description of batik recognition project	https://picsum.photos/720/480?random=7	{AI,Culture,"Computer Vision"}	public	published	019aabe5-142c-747d-8571-ee9cf89ae01a	2025-12-08 08:59:44.412682+00	2025-12-29 00:30:30.562702+00	This is a comprehensive AI project that uses deep learning to recognize and classify different batik patterns from Indonesian traditional textiles. The project aims to preserve cultural heritage through technology.	{Python,TensorFlow,OpenCV,FastAPI,PostgreSQL}	{"Dataset collection","Pattern complexity","Color variations"}	{"95% accuracy","Real-time processing","Mobile app integration"}	{"Expand dataset","3D pattern recognition","Cultural documentation"}	hard	2024-01-01 00:00:00+00	{https://demo1.example.com,https://prototype.example.com/v1,https://staging.project.com}
019b6793-a844-7397-a7b1-681da524eb10	Test Full Payload	test-full-payload	asdsadsa	https://spmb1.wempyaw.com/uploads/2025/12/000000002006_20251217_115103_251339.jpg	{}	public	draft	019aabe5-142c-747d-8571-ee9cf89ae01a	2025-12-29 00:48:08.772697+00	\N		{}	{}	{}	{}	medium	2025-12-29 00:42:53.409+00	{https://google.com/}
019b69a7-7962-78cc-ac43-90221389ddcd	asdsadasd	asdsadasd	asdsadsad	https://spmb1.wempyaw.com/uploads/2025/12/avatar-15_20251217_052327_657848.png	{}	public	published	019aabe5-142c-747d-8571-ee9cf89ae01a	2025-12-29 10:29:01.92479+00	2025-12-29 10:41:34.136086+00		{}	{}	{}	{}	medium	2025-12-29 00:00:00+00	{https://gmail.com/}
\.


--
-- Data for Name: project_category_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_category_links (id, project_id, category_id, created_at) FROM stdin;
019b69b2-7485-7276-8bff-9f77613449dd	019ae40f-c036-75c8-95f9-1cfdde24aea1	019aabe5-5991-7c7e-bf1a-5c2d41ad31a1	2025-12-29 10:41:01.573922+00
019b02f5-592e-7ae6-99fd-f0ce5fe6bfd0	019afd30-2d9c-78de-a48b-10c172214c9d	019aabe5-142c-747d-8571-ee9cf89ae01a	2025-12-09 11:53:12.238215+00
019b1007-2937-7d95-ae03-72ab2ce49b83	019ae400-8f72-7381-b71c-3a30aab2a55b	019aabe5-5991-7c7e-bf1a-5c2d41ad31a1	2025-12-12 00:47:43.415561+00
019b69b2-f3cb-7241-a1eb-e736ff061f17	019b69a7-7962-78cc-ac43-90221389ddcd	019aabe5-7647-75d1-9d2b-58a9fc0b35b8	2025-12-29 10:41:34.155692+00
\.


--
-- Data for Name: project_contributor_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_contributor_links (id, project_id, contributor_id, role_in_project, created_at) FROM stdin;
019b25b4-9f04-731d-84b3-a9c9c2dd0074	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b4-9d33-745a-a3a5-97da6a7f3839	Lead Developer	2025-12-16 05:49:12.836195+00
019b25b4-9f0b-761c-aeb9-ff50ddd04821	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b4-9d66-7d04-8c7d-785eaa1567dc	ML Engineer	2025-12-16 05:49:12.843862+00
019b25b4-9f10-76a3-983d-30fe7c13c418	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b4-9d96-754a-b470-5834fd920679	UI/UX Designer	2025-12-16 05:49:12.848964+00
019b25b6-56af-72c7-908e-8def701f7196	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b6-557d-7e4e-b1ec-9e4411b788b9	Lead Developer	2025-12-16 05:51:05.391566+00
019b25b6-56b5-7d5c-9ff1-88891ad5b95d	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b6-55a5-7a3a-a799-e1981f419600	ML Engineer	2025-12-16 05:51:05.397222+00
019b25b6-56bb-7297-83a0-73f61dae0a0d	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b6-55d0-7d07-9df2-10e456c63e11	UI/UX Designer	2025-12-16 05:51:05.403723+00
019b25b8-3217-7513-8110-8a51458ae65e	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b8-3071-7185-91e3-590b8dba5156	Lead Developer	2025-12-16 05:53:07.095308+00
019b25b8-321f-7ff4-ae8a-9a4211ed0375	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b8-30a5-7eea-843b-06feb60c57c3	ML Engineer	2025-12-16 05:53:07.103703+00
019b25b8-3225-73f7-a356-4b65d6f9e841	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b8-30d1-7c8c-a345-33abbe9d7d9e	UI/UX Designer	2025-12-16 05:53:07.109575+00
019b2a13-fbcf-7a38-a165-260a65ea3963	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b4-9d66-7d04-8c7d-785eaa1567dc	Lead Developer	2025-12-17 02:11:51.375537+00
019b2a13-fbd5-7959-97c9-9810bd9e0b17	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b4-9d33-745a-a3a5-97da6a7f3839	ML Engineer	2025-12-17 02:11:51.381456+00
019b2a18-ebc0-75ad-bd31-5ff3fb7e43c3	019b2a17-c756-74fa-9067-f517fef8d22e	019b25b4-9d66-7d04-8c7d-785eaa1567dc	Lead Developer	2025-12-17 02:17:14.94424+00
019b2a18-ebc8-73c8-9e90-e4f1d5b3061c	019b2a17-c756-74fa-9067-f517fef8d22e	019b25b4-9d33-745a-a3a5-97da6a7f3839	ML Engineer	2025-12-17 02:17:14.952573+00
019b2a4f-82ea-7cfe-80c7-0f13deff44ae	019afd30-2d9c-78de-a48b-10c172214c9d	019b25b8-3071-7185-91e3-590b8dba5156	Lead Developer	2025-12-17 03:16:52.586713+00
019b2a4f-c311-7c0e-a55d-7599d38c4bb1	019b2a17-c756-74fa-9067-f517fef8d22e	019b25b4-9d66-7d04-8c7d-785eaa1567dc	Lead Developer	2025-12-17 03:17:09.009137+00
019b2a4f-c318-796d-83bf-b00cd71d617a	019b2a17-c756-74fa-9067-f517fef8d22e	019b25b4-9d33-745a-a3a5-97da6a7f3839	ML Engineer	2025-12-17 03:17:09.016262+00
019b2a4f-c31e-7441-b6d3-b8f0371178e3	019b2a17-c756-74fa-9067-f517fef8d22e	019b25b6-55a5-7a3a-a799-e1981f419600	hghh	2025-12-17 03:17:09.023049+00
019b2a53-e150-793d-8275-782226202e5c	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b4-9d66-7d04-8c7d-785eaa1567dc	a	2025-12-17 03:21:38.896678+00
019b2a53-e156-7931-a045-11593de59673	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b4-9d33-745a-a3a5-97da6a7f3839	b	2025-12-17 03:21:38.903029+00
019b2a54-1a87-7f5e-965b-84459341fb2c	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b4-9d66-7d04-8c7d-785eaa1567dc	a	2025-12-17 03:21:53.54343+00
019b2a54-1a8f-76f9-8170-4da4e0416a0d	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b4-9d33-745a-a3a5-97da6a7f3839	b	2025-12-17 03:21:53.552069+00
019b2a54-1a98-783f-b241-77dd16661c76	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b6-55a5-7a3a-a799-e1981f419600	c	2025-12-17 03:21:53.560316+00
019b2a54-1aa0-7737-acda-da2261eec810	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b6-557d-7e4e-b1ec-9e4411b788b9	d	2025-12-17 03:21:53.568267+00
019b2a54-53bc-7590-84a8-082739a813e5	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b4-9d66-7d04-8c7d-785eaa1567dc	a	2025-12-17 03:22:08.188496+00
019b2a54-53c3-76d3-8440-8d308a325ecf	019b2a53-af29-7c4e-b2e7-84812aadb185	019b25b4-9d33-745a-a3a5-97da6a7f3839	b	2025-12-17 03:22:08.196053+00
019b396f-fc05-78fb-8c92-faff24c45cbf	019ae40f-c036-75c8-95f9-1cfdde24aea1	019b25b8-3071-7185-91e3-590b8dba5156		2025-12-20 01:46:38.981745+00
019b3a5d-f7f2-7127-b3d8-cbc7b70906ad	019b3a3f-1167-732d-9f54-73906ed0b461	019b25b8-3071-7185-91e3-590b8dba5156	A	2025-12-20 06:06:35.506716+00
019b69a8-9955-78fe-94b1-b8d9b45c944a	019b69a7-7962-78cc-ac43-90221389ddcd	019b25b4-9d33-745a-a3a5-97da6a7f3839		2025-12-29 10:30:15.637477+00
019b69a8-995e-7cf6-8679-82695fe38b6c	019b69a7-7962-78cc-ac43-90221389ddcd	019b25b8-3071-7185-91e3-590b8dba5156		2025-12-29 10:30:15.647064+00
\.


--
-- Data for Name: publication_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.publication_categories (id, name, slug, description, created_at) FROM stdin;
019abb08-a8ec-75f5-baff-4e8a83f267e1	Machine Learning	machine-learning	Research related to machine learning algorithms and techniques	2025-11-25 12:41:38.284855+00
019abb08-d3a1-7408-92c6-2df0e527502e	Computer Vision	computer-vision	Research in image processing and computer vision	2025-11-25 12:41:49.217992+00
\.


--
-- Data for Name: publications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.publications (id, title, slug, abstract, pdf_url, journal_name, year, graphical_abstract_url, access_level, status, created_by, created_at, updated_at, authors, venue, citations, doi, keywords, impact, pages, volume, issue, publisher, methodology, results, conclusions, view_count, download_count) FROM stdin;
019ae469-7627-7a6f-ae4f-8aae5cc42513	Advanced ML for Computer Vision	advanced-ml-for-computer-vision	This paper presents novel approaches to machine learning in computer vision applications	https://s2.q4cdn.com/175719177/files/doc_presentations/Placeholder-PDF.pdf	IEEE Transactions on Pattern Analysis and Machine Intelligence	2024	https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjLUwgn9qUntcjl0RbjNTTttVCu83yOIXgQg&s	public	published	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-03 13:31:48.135728+00	2025-12-20 01:16:53.334155+00	{"Dr. John Smith","Prof. Jane Doe","Dr. Mike Johnson",asdasdad}	IEEE Conference on Computer Vision and Pattern Recognition	25	10.1109/CVPR.2024.12345	{"machine learning","computer vision","deep learning","neural networks","attention mechanisms"}	5.2	123-135	42	3	IEEE Press	UPDATED: We employed deep convolutional neural networks with enhanced attention mechanisms and transfer learning	UPDATED: Our improved method achieved 97% accuracy on standard benchmarks	UPDATED: The enhanced approach significantly outperforms all existing methods	31	5
019b1504-ea9f-7b9a-b167-bee2f34cb44f	A Decade Survey of Content Based Image Retrieval Using Deep Learning	a-decade-survey-of-content-based-image-retrieval-using-deep-learning	The content based image retrieval aims to find the similar images from a large scale dataset against a query image. Generally, the similarity between the representative features of the query image and dataset images is used to rank the images for retrieval. In early days, various hand designed feature descriptors have been investigated based on the visual cues such as color, texture, shape, etc. that represent the images. However, the deep learning has emerged as a dominating alternative of hand-designed feature engineering from a decade. It learns the features automatically from the data.	https://s2.q4cdn.com/175719177/files/doc_presentations/Placeholder-PDF.pdf	IEEE	2016	https://picsum.photos/200/300?random=2	public	published	019aac02-ac77-7338-ac5b-3a8446f4a76d	2025-12-13 00:03:22.399857+00	2025-12-23 04:37:41.68287+00	{"Shiv Ram Dubey"}	IEEE	22	10.1109/TCSVT.2021.3080920	{"Image retrieval","Deep learning"}	2.2	120-140	14	2	IEEE	This paper presents a comprehensive survey of deep learning based developments in the past decade for content based image retrieval. The categorization of existing state-of-the-art methods from different perspectives is also performed for greater understanding of the progress. The taxonomy used in this survey covers different supervision, different networks, different descriptor type and different retrieval type.	A performance analysis is also performed using the state-of-the-art methods. The insights are also presented for the benefit of the researchers to observe the progress and to make the best choices.	The survey presented in this paper will help in further research progress in image retrieval using deep learning.	12	1
\.


--
-- Data for Name: publication_category_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.publication_category_links (id, publication_id, category_id, created_at) FROM stdin;
019b02ea-622f-7fc3-93d2-2d982769f0fa	019ae469-7627-7a6f-ae4f-8aae5cc42513	019abb08-a8ec-75f5-baff-4e8a83f267e1	2025-12-09 11:41:13.64787+00
\.


--
-- Data for Name: publication_contributor_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.publication_contributor_links (id, publication_id, contributor_id, role_in_publication, created_at) FROM stdin;
\.


--
-- Data for Name: rate_limit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rate_limit (id, tier_id, name, path, "limit", period, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscriptions (id, user_id, plan_name, price, start_date, end_date, status, payment_ref, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: token_blacklist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.token_blacklist (id, token, expires_at) FROM stdin;
1	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdXBlcm5ld0BleGFtcGxlLmNvbSIsImV4cCI6MTc2NDY1NDA2MCwidG9rZW5fdHlwZSI6ImFjY2VzcyJ9.jq0YitcfLD4_G9RqzsgO3fAb4BD14XkDUbsm1KC1RFk	2025-12-02 05:41:00
2	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdXBlcm5ld0BleGFtcGxlLmNvbSIsImV4cCI6MTc2NTI1NzA2MCwidG9rZW5fdHlwZSI6InJlZnJlc2gifQ.eh_VATK0S5FslNjdkAq8QVHXGariZI4scuDO-iVWhfU	2025-12-09 05:11:00
\.


--
-- Name: post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.post_id_seq', 1, false);


--
-- Name: rate_limit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rate_limit_id_seq', 1, false);


--
-- Name: tier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tier_id_seq', 1, false);


--
-- Name: token_blacklist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.token_blacklist_id_seq', 2, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict o0wGLEVhv1BR3wyuIYPpUJsgN4PxsBrb4sc207A7reDLRpCBuujk59fM6nxqpf3

