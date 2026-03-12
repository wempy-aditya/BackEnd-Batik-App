--
-- PostgreSQL database dump
--

\restrict 4lA7CrWgIuYw2FBGmKFDBpOraBVMFcGkPiskuU8YqSKgZfVoBitcpIRbBaPp0Fq

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
-- Name: accesslevel; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.accesslevel AS ENUM (
    'public',
    'registered',
    'premium'
);


ALTER TYPE public.accesslevel OWNER TO postgres;

--
-- Name: contentstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.contentstatus AS ENUM (
    'draft',
    'published'
);


ALTER TYPE public.contentstatus OWNER TO postgres;

--
-- Name: projectcomplexity; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.projectcomplexity AS ENUM (
    'easy',
    'medium',
    'hard'
);


ALTER TYPE public.projectcomplexity OWNER TO postgres;

--
-- Name: subscriptionstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.subscriptionstatus AS ENUM (
    'active',
    'expired',
    'pending'
);


ALTER TYPE public.subscriptionstatus OWNER TO postgres;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.userrole AS ENUM (
    'admin',
    'registered',
    'premium'
);


ALTER TYPE public.userrole OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: contributors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contributors (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255),
    role character varying(100),
    bio text,
    profile_image text,
    github_url text,
    linkedin_url text,
    website_url text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.contributors OWNER TO postgres;

--
-- Name: dataset_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dataset_categories (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description character varying,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.dataset_categories OWNER TO postgres;

--
-- Name: dataset_category_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dataset_category_links (
    id uuid NOT NULL,
    dataset_id uuid NOT NULL,
    category_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.dataset_category_links OWNER TO postgres;

--
-- Name: dataset_contributor_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dataset_contributor_links (
    id uuid NOT NULL,
    dataset_id uuid NOT NULL,
    contributor_id uuid NOT NULL,
    role_in_dataset character varying(100),
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.dataset_contributor_links OWNER TO postgres;

--
-- Name: datasets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datasets (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    sample_image_url text,
    file_url text,
    source character varying(255),
    size bigint,
    access_level public.accesslevel NOT NULL,
    status public.contentstatus NOT NULL,
    created_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    tagline character varying(500),
    samples integer,
    download_count integer DEFAULT 0 NOT NULL,
    gradient character varying(100),
    version character varying(50),
    format character varying(100),
    license character varying(255),
    citation text,
    key_features character varying[],
    use_cases character varying[],
    technical_specs jsonb,
    statistics jsonb,
    sample_images character varying[],
    view_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.datasets OWNER TO postgres;

--
-- Name: files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.files (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    original_filename character varying(255) NOT NULL,
    filename character varying(255) NOT NULL,
    file_path text NOT NULL,
    file_url text NOT NULL,
    file_type character varying(50) NOT NULL,
    mime_type character varying(100) NOT NULL,
    file_size integer NOT NULL,
    uploaded_by uuid,
    file_metadata text,
    description text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.files OWNER TO postgres;

--
-- Name: gallery; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gallery (
    id uuid NOT NULL,
    prompt text,
    image_url text,
    extra_metadata jsonb,
    model_id uuid,
    created_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.gallery OWNER TO postgres;

--
-- Name: gallery_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gallery_categories (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description character varying,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.gallery_categories OWNER TO postgres;

--
-- Name: gallery_category_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gallery_category_links (
    id uuid NOT NULL,
    gallery_id uuid NOT NULL,
    category_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.gallery_category_links OWNER TO postgres;

--
-- Name: model_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model_categories (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description character varying,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.model_categories OWNER TO postgres;

--
-- Name: model_category_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model_category_links (
    id uuid NOT NULL,
    model_id uuid NOT NULL,
    category_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.model_category_links OWNER TO postgres;

--
-- Name: models; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.models (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    architecture character varying(255),
    dataset_used character varying(255),
    metrics jsonb,
    model_file_url text,
    access_level public.accesslevel NOT NULL,
    status public.contentstatus NOT NULL,
    created_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.models OWNER TO postgres;

--
-- Name: news; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    content text,
    thumbnail_url text,
    tags character varying[],
    access_level public.accesslevel NOT NULL,
    status public.contentstatus NOT NULL,
    created_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.news OWNER TO postgres;

--
-- Name: news_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_categories (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description character varying,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.news_categories OWNER TO postgres;

--
-- Name: news_category_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_category_links (
    id uuid NOT NULL,
    news_id uuid NOT NULL,
    category_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.news_category_links OWNER TO postgres;

--
-- Name: post; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.post (
    id integer NOT NULL,
    created_by_user_id integer NOT NULL,
    title character varying(30) NOT NULL,
    text character varying(63206) NOT NULL,
    uuid uuid NOT NULL,
    media_url character varying,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    is_deleted boolean NOT NULL
);


ALTER TABLE public.post OWNER TO postgres;

--
-- Name: post_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_id_seq OWNER TO postgres;

--
-- Name: post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;


--
-- Name: project_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_categories (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description character varying,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.project_categories OWNER TO postgres;

--
-- Name: project_category_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_category_links (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    category_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.project_category_links OWNER TO postgres;

--
-- Name: project_contributor_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_contributor_links (
    id uuid NOT NULL,
    project_id uuid NOT NULL,
    contributor_id uuid NOT NULL,
    role_in_project character varying(100),
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.project_contributor_links OWNER TO postgres;

--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    thumbnail_url text,
    tags character varying[],
    access_level public.accesslevel NOT NULL,
    status public.contentstatus NOT NULL,
    created_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    full_description text,
    technologies character varying[],
    challenges character varying[],
    achievements character varying[],
    future_work character varying[],
    complexity public.projectcomplexity,
    start_at timestamp with time zone,
    demo_url text[]
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: publication_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publication_categories (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description character varying,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.publication_categories OWNER TO postgres;

--
-- Name: publication_category_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publication_category_links (
    id uuid NOT NULL,
    publication_id uuid NOT NULL,
    category_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.publication_category_links OWNER TO postgres;

--
-- Name: publication_contributor_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publication_contributor_links (
    id uuid NOT NULL,
    publication_id uuid NOT NULL,
    contributor_id uuid NOT NULL,
    role_in_publication character varying(100),
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.publication_contributor_links OWNER TO postgres;

--
-- Name: publications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publications (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    abstract text,
    pdf_url text,
    journal_name character varying(255),
    year integer,
    graphical_abstract_url text,
    access_level public.accesslevel NOT NULL,
    status public.contentstatus NOT NULL,
    created_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    authors character varying[],
    venue character varying(255),
    citations integer,
    doi character varying(255),
    keywords character varying[],
    impact character varying(50),
    pages character varying(50),
    volume character varying(50),
    issue character varying(50),
    publisher character varying(255),
    methodology text,
    results text,
    conclusions text,
    view_count integer DEFAULT 0 NOT NULL,
    download_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.publications OWNER TO postgres;

--
-- Name: rate_limit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rate_limit (
    id integer NOT NULL,
    tier_id integer NOT NULL,
    name character varying NOT NULL,
    path character varying NOT NULL,
    "limit" integer NOT NULL,
    period integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.rate_limit OWNER TO postgres;

--
-- Name: rate_limit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rate_limit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rate_limit_id_seq OWNER TO postgres;

--
-- Name: rate_limit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rate_limit_id_seq OWNED BY public.rate_limit.id;


--
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscriptions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    plan_name character varying(100) NOT NULL,
    price numeric(10,2) NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone NOT NULL,
    status public.subscriptionstatus NOT NULL,
    payment_ref character varying(255),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.subscriptions OWNER TO postgres;

--
-- Name: tier; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tier (
    id integer NOT NULL,
    name character varying NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.tier OWNER TO postgres;

--
-- Name: tier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tier_id_seq OWNER TO postgres;

--
-- Name: tier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tier_id_seq OWNED BY public.tier.id;


--
-- Name: token_blacklist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.token_blacklist (
    id integer NOT NULL,
    token character varying NOT NULL,
    expires_at timestamp without time zone NOT NULL
);


ALTER TABLE public.token_blacklist OWNER TO postgres;

--
-- Name: token_blacklist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.token_blacklist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_blacklist_id_seq OWNER TO postgres;

--
-- Name: token_blacklist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.token_blacklist_id_seq OWNED BY public.token_blacklist.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    username character varying(20) NOT NULL,
    email character varying(50) NOT NULL,
    hashed_password character varying NOT NULL,
    profile_image_url character varying NOT NULL,
    uuid uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    is_deleted boolean NOT NULL,
    is_superuser boolean NOT NULL,
    tier_id integer
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying NOT NULL,
    role public.userrole NOT NULL,
    is_active boolean NOT NULL,
    is_deleted boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    username character varying(50),
    profile_image_url character varying,
    deleted_at timestamp with time zone,
    is_superuser boolean NOT NULL,
    tier_id integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: post id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post ALTER COLUMN id SET DEFAULT nextval('public.post_id_seq'::regclass);


--
-- Name: rate_limit id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rate_limit ALTER COLUMN id SET DEFAULT nextval('public.rate_limit_id_seq'::regclass);


--
-- Name: tier id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tier ALTER COLUMN id SET DEFAULT nextval('public.tier_id_seq'::regclass);


--
-- Name: token_blacklist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist ALTER COLUMN id SET DEFAULT nextval('public.token_blacklist_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: contributors contributors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contributors
    ADD CONSTRAINT contributors_pkey PRIMARY KEY (id);


--
-- Name: dataset_categories dataset_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dataset_categories
    ADD CONSTRAINT dataset_categories_pkey PRIMARY KEY (id);


--
-- Name: dataset_category_links dataset_category_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dataset_category_links
    ADD CONSTRAINT dataset_category_links_pkey PRIMARY KEY (id);


--
-- Name: dataset_contributor_links dataset_contributor_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dataset_contributor_links
    ADD CONSTRAINT dataset_contributor_links_pkey PRIMARY KEY (id);


--
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id);


--
-- Name: files files_filename_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_filename_key UNIQUE (filename);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: gallery_categories gallery_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery_categories
    ADD CONSTRAINT gallery_categories_pkey PRIMARY KEY (id);


--
-- Name: gallery_category_links gallery_category_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery_category_links
    ADD CONSTRAINT gallery_category_links_pkey PRIMARY KEY (id);


--
-- Name: gallery gallery_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery
    ADD CONSTRAINT gallery_pkey PRIMARY KEY (id);


--
-- Name: model_categories model_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_categories
    ADD CONSTRAINT model_categories_pkey PRIMARY KEY (id);


--
-- Name: model_category_links model_category_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_category_links
    ADD CONSTRAINT model_category_links_pkey PRIMARY KEY (id);


--
-- Name: models models_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_pkey PRIMARY KEY (id);


--
-- Name: news_categories news_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_categories
    ADD CONSTRAINT news_categories_pkey PRIMARY KEY (id);


--
-- Name: news_category_links news_category_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_category_links
    ADD CONSTRAINT news_category_links_pkey PRIMARY KEY (id);


--
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (id);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: post post_uuid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_uuid_key UNIQUE (uuid);


--
-- Name: project_categories project_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_categories
    ADD CONSTRAINT project_categories_pkey PRIMARY KEY (id);


--
-- Name: project_category_links project_category_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_category_links
    ADD CONSTRAINT project_category_links_pkey PRIMARY KEY (id);


--
-- Name: project_contributor_links project_contributor_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_contributor_links
    ADD CONSTRAINT project_contributor_links_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: publication_categories publication_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_categories
    ADD CONSTRAINT publication_categories_pkey PRIMARY KEY (id);


--
-- Name: publication_category_links publication_category_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_category_links
    ADD CONSTRAINT publication_category_links_pkey PRIMARY KEY (id);


--
-- Name: publication_contributor_links publication_contributor_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_contributor_links
    ADD CONSTRAINT publication_contributor_links_pkey PRIMARY KEY (id);


--
-- Name: publications publications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_pkey PRIMARY KEY (id);


--
-- Name: rate_limit rate_limit_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rate_limit
    ADD CONSTRAINT rate_limit_name_key UNIQUE (name);


--
-- Name: rate_limit rate_limit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rate_limit
    ADD CONSTRAINT rate_limit_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: tier tier_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tier
    ADD CONSTRAINT tier_name_key UNIQUE (name);


--
-- Name: tier tier_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tier
    ADD CONSTRAINT tier_pkey PRIMARY KEY (id);


--
-- Name: token_blacklist token_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist
    ADD CONSTRAINT token_blacklist_pkey PRIMARY KEY (id);


--
-- Name: dataset_category_links unique_dataset_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dataset_category_links
    ADD CONSTRAINT unique_dataset_category UNIQUE (dataset_id, category_id);


--
-- Name: gallery_category_links unique_gallery_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery_category_links
    ADD CONSTRAINT unique_gallery_category UNIQUE (gallery_id, category_id);


--
-- Name: model_category_links unique_model_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_category_links
    ADD CONSTRAINT unique_model_category UNIQUE (model_id, category_id);


--
-- Name: news_category_links unique_news_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_category_links
    ADD CONSTRAINT unique_news_category UNIQUE (news_id, category_id);


--
-- Name: project_category_links unique_project_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_category_links
    ADD CONSTRAINT unique_project_category UNIQUE (project_id, category_id);


--
-- Name: publication_category_links unique_publication_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_category_links
    ADD CONSTRAINT unique_publication_category UNIQUE (publication_id, category_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_uuid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_uuid_key UNIQUE (uuid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_dataset_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_dataset_categories_slug ON public.dataset_categories USING btree (slug);


--
-- Name: ix_dataset_category_links_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_dataset_category_links_category_id ON public.dataset_category_links USING btree (category_id);


--
-- Name: ix_dataset_category_links_dataset_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_dataset_category_links_dataset_id ON public.dataset_category_links USING btree (dataset_id);


--
-- Name: ix_datasets_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_datasets_created_by ON public.datasets USING btree (created_by);


--
-- Name: ix_datasets_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_datasets_slug ON public.datasets USING btree (slug);


--
-- Name: ix_files_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_files_created_at ON public.files USING btree (created_at);


--
-- Name: ix_files_file_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_files_file_type ON public.files USING btree (file_type);


--
-- Name: ix_files_filename; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_files_filename ON public.files USING btree (filename);


--
-- Name: ix_files_uploaded_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_files_uploaded_by ON public.files USING btree (uploaded_by);


--
-- Name: ix_gallery_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_gallery_categories_slug ON public.gallery_categories USING btree (slug);


--
-- Name: ix_gallery_category_links_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_gallery_category_links_category_id ON public.gallery_category_links USING btree (category_id);


--
-- Name: ix_gallery_category_links_gallery_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_gallery_category_links_gallery_id ON public.gallery_category_links USING btree (gallery_id);


--
-- Name: ix_gallery_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_gallery_created_by ON public.gallery USING btree (created_by);


--
-- Name: ix_gallery_model_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_gallery_model_id ON public.gallery USING btree (model_id);


--
-- Name: ix_model_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_model_categories_slug ON public.model_categories USING btree (slug);


--
-- Name: ix_model_category_links_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_model_category_links_category_id ON public.model_category_links USING btree (category_id);


--
-- Name: ix_model_category_links_model_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_model_category_links_model_id ON public.model_category_links USING btree (model_id);


--
-- Name: ix_models_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_models_created_by ON public.models USING btree (created_by);


--
-- Name: ix_models_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_models_slug ON public.models USING btree (slug);


--
-- Name: ix_news_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_news_categories_slug ON public.news_categories USING btree (slug);


--
-- Name: ix_news_category_links_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_news_category_links_category_id ON public.news_category_links USING btree (category_id);


--
-- Name: ix_news_category_links_news_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_news_category_links_news_id ON public.news_category_links USING btree (news_id);


--
-- Name: ix_news_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_news_created_by ON public.news USING btree (created_by);


--
-- Name: ix_news_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_news_slug ON public.news USING btree (slug);


--
-- Name: ix_post_created_by_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_post_created_by_user_id ON public.post USING btree (created_by_user_id);


--
-- Name: ix_post_is_deleted; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_post_is_deleted ON public.post USING btree (is_deleted);


--
-- Name: ix_project_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_project_categories_slug ON public.project_categories USING btree (slug);


--
-- Name: ix_project_category_links_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_project_category_links_category_id ON public.project_category_links USING btree (category_id);


--
-- Name: ix_project_category_links_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_project_category_links_project_id ON public.project_category_links USING btree (project_id);


--
-- Name: ix_projects_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_projects_created_by ON public.projects USING btree (created_by);


--
-- Name: ix_projects_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_projects_slug ON public.projects USING btree (slug);


--
-- Name: ix_publication_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_publication_categories_slug ON public.publication_categories USING btree (slug);


--
-- Name: ix_publication_category_links_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_publication_category_links_category_id ON public.publication_category_links USING btree (category_id);


--
-- Name: ix_publication_category_links_publication_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_publication_category_links_publication_id ON public.publication_category_links USING btree (publication_id);


--
-- Name: ix_publications_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_publications_created_by ON public.publications USING btree (created_by);


--
-- Name: ix_publications_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_publications_slug ON public.publications USING btree (slug);


--
-- Name: ix_rate_limit_tier_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_rate_limit_tier_id ON public.rate_limit USING btree (tier_id);


--
-- Name: ix_subscriptions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_subscriptions_user_id ON public.subscriptions USING btree (user_id);


--
-- Name: ix_token_blacklist_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_token_blacklist_token ON public.token_blacklist USING btree (token);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_is_deleted; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_is_deleted ON public."user" USING btree (is_deleted);


--
-- Name: ix_user_tier_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_tier_id ON public."user" USING btree (tier_id);


--
-- Name: ix_user_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_username ON public."user" USING btree (username);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_is_deleted; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_is_deleted ON public.users USING btree (is_deleted);


--
-- Name: ix_users_tier_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_tier_id ON public.users USING btree (tier_id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: dataset_category_links dataset_category_links_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dataset_category_links
    ADD CONSTRAINT dataset_category_links_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.dataset_categories(id);


--
-- Name: dataset_category_links dataset_category_links_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dataset_category_links
    ADD CONSTRAINT dataset_category_links_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.datasets(id);


--
-- Name: datasets datasets_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: files files_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: gallery_category_links gallery_category_links_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery_category_links
    ADD CONSTRAINT gallery_category_links_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.gallery_categories(id);


--
-- Name: gallery_category_links gallery_category_links_gallery_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery_category_links
    ADD CONSTRAINT gallery_category_links_gallery_id_fkey FOREIGN KEY (gallery_id) REFERENCES public.gallery(id);


--
-- Name: gallery gallery_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery
    ADD CONSTRAINT gallery_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: gallery gallery_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gallery
    ADD CONSTRAINT gallery_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.models(id);


--
-- Name: model_category_links model_category_links_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_category_links
    ADD CONSTRAINT model_category_links_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.model_categories(id);


--
-- Name: model_category_links model_category_links_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_category_links
    ADD CONSTRAINT model_category_links_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.models(id);


--
-- Name: models models_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: news_category_links news_category_links_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_category_links
    ADD CONSTRAINT news_category_links_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.news_categories(id);


--
-- Name: news_category_links news_category_links_news_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_category_links
    ADD CONSTRAINT news_category_links_news_id_fkey FOREIGN KEY (news_id) REFERENCES public.news(id);


--
-- Name: news news_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: post post_created_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_created_by_user_id_fkey FOREIGN KEY (created_by_user_id) REFERENCES public."user"(id);


--
-- Name: project_category_links project_category_links_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_category_links
    ADD CONSTRAINT project_category_links_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.project_categories(id);


--
-- Name: project_category_links project_category_links_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_category_links
    ADD CONSTRAINT project_category_links_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: projects projects_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: publication_category_links publication_category_links_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_category_links
    ADD CONSTRAINT publication_category_links_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.publication_categories(id);


--
-- Name: publication_category_links publication_category_links_publication_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publication_category_links
    ADD CONSTRAINT publication_category_links_publication_id_fkey FOREIGN KEY (publication_id) REFERENCES public.publications(id);


--
-- Name: publications publications_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: rate_limit rate_limit_tier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rate_limit
    ADD CONSTRAINT rate_limit_tier_id_fkey FOREIGN KEY (tier_id) REFERENCES public.tier(id);


--
-- Name: subscriptions subscriptions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user user_tier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_tier_id_fkey FOREIGN KEY (tier_id) REFERENCES public.tier(id);


--
-- Name: users users_tier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_tier_id_fkey FOREIGN KEY (tier_id) REFERENCES public.tier(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 4lA7CrWgIuYw2FBGmKFDBpOraBVMFcGkPiskuU8YqSKgZfVoBitcpIRbBaPp0Fq

