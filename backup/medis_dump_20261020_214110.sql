--
-- PostgreSQL database dump
--

\restrict WJlD72s0njRM9SFcPgnUW7mo2TiunUtJTgpMRYoDsvt4AgF2Hwk0ghdlaF0IFVJ

-- Dumped from database version 16.15
-- Dumped by pg_dump version 16.15

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
-- Name: pasien; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pasien (
    id integer NOT NULL,
    nama text NOT NULL
);


ALTER TABLE public.pasien OWNER TO postgres;

--
-- Name: pasien_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pasien_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pasien_id_seq OWNER TO postgres;

--
-- Name: pasien_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pasien_id_seq OWNED BY public.pasien.id;


--
-- Name: pasien id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pasien ALTER COLUMN id SET DEFAULT nextval('public.pasien_id_seq'::regclass);


--
-- Data for Name: pasien; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pasien (id, nama) FROM stdin;
1	Pasien Contoh 01
2	Pasien Contoh 02
3	Pasien Contoh 03
\.


--
-- Name: pasien_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pasien_id_seq', 33, true);


--
-- Name: pasien pasien_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pasien
    ADD CONSTRAINT pasien_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict WJlD72s0njRM9SFcPgnUW7mo2TiunUtJTgpMRYoDsvt4AgF2Hwk0ghdlaF0IFVJ

