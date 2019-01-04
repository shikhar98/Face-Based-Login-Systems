--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 11.1 (Ubuntu 11.1-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: names; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.names (id, name) FROM stdin;
1	Shikhar
2	Siddharth Sir
3	Dhanu
4	Akshay Kumar
\.


--
-- Name: names_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.names_id_seq', 5, true);


--
-- PostgreSQL database dump complete
--

