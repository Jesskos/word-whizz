--
-- PostgreSQL database dump
--

-- Dumped from database version 11.0
-- Dumped by pg_dump version 11.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.scores DROP CONSTRAINT scores_user_id_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.scores DROP CONSTRAINT scores_pkey;
ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE public.scores ALTER COLUMN score_id DROP DEFAULT;
DROP SEQUENCE public.users_user_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.scores_score_id_seq;
DROP TABLE public.scores;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: scores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scores (
    score_id integer NOT NULL,
    user_id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    word character varying(20) NOT NULL,
    score integer NOT NULL,
    won boolean NOT NULL
);


--
-- Name: scores_score_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.scores_score_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: scores_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.scores_score_id_seq OWNED BY public.scores.score_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: scores score_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scores ALTER COLUMN score_id SET DEFAULT nextval('public.scores_score_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: scores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.scores (score_id, user_id, date, word, score, won) FROM stdin;
1	1	2018-11-23 20:10:56.450667	cellars	102	f
2	1	2018-11-23 20:13:25.035894	fessing	162	f
3	1	2018-11-23 20:16:26.630326	nowt	4	f
4	1	2018-11-23 20:32:36.924163	vine	24	f
5	1	2018-11-23 20:34:10.024299	heads	60	t
6	1	2018-11-23 20:34:55.083304	tad	14	f
7	1	2018-11-23 20:36:19.647999	meatier	70	t
8	1	2018-11-23 20:48:33.538308	gurney	12	f
9	1	2018-11-23 20:51:52.355801	goofy	147	t
10	1	2018-11-23 20:53:01.806712	stinger	80	t
11	2	2018-11-23 22:46:57.632226	huddler	102	f
12	2	2018-11-23 22:48:04.243914	sunns	14	f
13	2	2018-11-23 22:48:49.899086	macaco	250	t
14	3	2018-11-23 22:50:58.35732	nebulae	210	t
15	4	2018-11-23 22:52:08.163581	dammar	147	t
16	4	2018-11-23 22:53:47.223548	rebegan	201	t
17	1	2018-11-23 23:02:06.59095	oldstyle	225	t
18	1	2018-11-23 23:04:56.30122	songstress	162	f
19	1	2018-11-23 23:06:57.986643	grimier	42	f
20	1	2018-11-23 23:12:16.831803	extort	102	f
21	1	2018-11-23 23:14:48.029704	chiros	48	f
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, username, password) FROM stdin;
1	akhil	123
2	jess	12345
3	zoe	123
4	funguesser	12345
\.


--
-- Name: scores_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.scores_score_id_seq', 21, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 4, true);


--
-- Name: scores scores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_pkey PRIMARY KEY (score_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: scores scores_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

