--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: analyticsdb_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.analyticsdb_events (
    event text,
    page text,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.analyticsdb_events OWNER TO postgres;

--
-- Name: games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.games (
    id integer NOT NULL,
    name character varying(255),
    category character varying(255),
    release_date date,
    price double precision
);


ALTER TABLE public.games OWNER TO postgres;

--
-- Name: games_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.games_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.games_id_seq OWNER TO postgres;

--
-- Name: games_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.games_id_seq OWNED BY public.games.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    cart_items jsonb,
    total_price double precision,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: games id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games ALTER COLUMN id SET DEFAULT nextval('public.games_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Data for Name: analyticsdb_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.analyticsdb_events (event, page, "timestamp") FROM stdin;
session_end	/index.html	2025-08-09 04:41:34
page_view	/index.html	2025-08-09 04:41:35
click	/index.html	2025-08-09 04:42:11
session_end	/index.html	2025-08-09 04:42:11
page_view	/index.html	2025-08-09 04:42:15
test_event	test_page	2025-08-09 05:04:08
page_view	/index.html	2025-08-09 05:04:29
click	/index.html	2025-08-09 05:05:32
session_end	/index.html	2025-08-09 05:05:32
page_view	/index.html	2025-08-09 05:07:32
\.


--
-- Data for Name: games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.games (id, name, category, release_date, price) FROM stdin;
1	Test Game	Action	2025-01-01	29.99
2	Another Game	Adventure	2025-02-01	49.99
3	New Game	RPG	2025-03-01	59.99
4	New Game	RPG	2025-03-01	59.99
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, cart_items, total_price, created_at) FROM stdin;
1	[{"qty": 2, "item": "T-shirt"}]	39.98	2025-08-08 07:22:33.105405
2	[{"qty": 1, "item": "Cap"}]	15.99	2025-08-08 07:38:59.536378
3	[{"qty": 1, "item": "Cap"}]	15.99	2025-08-08 14:24:44.96609
4	[{"qty": 1, "item": "Shirt"}]	19.99	2025-08-08 16:25:53.09711
5	[{"qty": 1, "item": "Shirt"}]	19.99	2025-08-09 04:43:23.339634
\.


--
-- Name: games_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.games_id_seq', 4, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 5, true);


--
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

