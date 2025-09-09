--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Homebrew)
-- Dumped by pg_dump version 14.15 (Homebrew)

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
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: national_id_types; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.national_id_types AS ENUM (
    'CURP',
    'SSN',
    'DNI',
    'CEDULA',
    'RUN',
    'SIN',
    'OTHER'
);


--
-- Name: tax_id_types; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tax_id_types AS ENUM (
    'RFC',
    'TIN',
    'SSN',
    'NIF',
    'RNC',
    'RUT',
    'SIN',
    'BN',
    'OTHER'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: answers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answers (
    id bigint NOT NULL,
    procedure_id integer,
    name character varying(255),
    value text,
    user_id integer,
    status integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);


--
-- Name: answers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.answers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.answers_id_seq OWNED BY public.answers.id;


--
-- Name: answers_json; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answers_json (
    id bigint NOT NULL,
    procedure_id integer NOT NULL,
    user_id integer NOT NULL,
    answers json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: answers_json_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.answers_json_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: answers_json_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.answers_json_id_seq OWNED BY public.answers_json.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: base_administrative_division; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.base_administrative_division (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(5) NOT NULL,
    division_type character varying(50),
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: base_administrative_division_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.base_administrative_division_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: base_administrative_division_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.base_administrative_division_id_seq OWNED BY public.base_administrative_division.id;


--
-- Name: base_locality; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.base_locality (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    scope character varying(15) NOT NULL,
    municipality_code character varying(5) NOT NULL,
    locality_code character varying(8) NOT NULL,
    geocode character varying(12) NOT NULL,
    municipality_id integer NOT NULL,
    geom public.geometry(MultiPolygon,4326),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'MULTIPOLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 4326))
);


--
-- Name: base_locality_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.base_locality_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: base_locality_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.base_locality_id_seq OWNED BY public.base_locality.id;


--
-- Name: base_map_layer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.base_map_layer (
    id integer NOT NULL,
    value character varying(100) NOT NULL,
    label character varying(180) NOT NULL,
    type character varying(20) NOT NULL,
    url character varying(255) NOT NULL,
    layers character varying(60) NOT NULL,
    visible boolean NOT NULL,
    active boolean NOT NULL,
    attribution character varying(100),
    opacity numeric(3,2) NOT NULL,
    server_type character varying(60),
    projection character varying(20) NOT NULL,
    version character varying(10) NOT NULL,
    format character varying(60) NOT NULL,
    "order" integer NOT NULL,
    editable boolean NOT NULL,
    type_geom character varying(20),
    cql_filter character varying(255)
);


--
-- Name: base_map_layer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.base_map_layer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: base_map_layer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.base_map_layer_id_seq OWNED BY public.base_map_layer.id;


--
-- Name: base_municipality; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.base_municipality (
    id integer NOT NULL,
    municipality_id integer NOT NULL,
    name character varying(255) NOT NULL,
    entity_code character varying(5) NOT NULL,
    municipality_code character varying(5) NOT NULL,
    geocode character varying(10) NOT NULL,
    has_zoning boolean NOT NULL,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: base_municipality_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.base_municipality_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: base_municipality_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.base_municipality_id_seq OWNED BY public.base_municipality.id;


--
-- Name: base_neighborhood; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.base_neighborhood (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    postal_code character varying(20),
    locality_id integer,
    municipality_id integer NOT NULL,
    geom public.geometry(MultiPolygon,4326),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'MULTIPOLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 4326))
);


--
-- Name: base_neighborhood_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.base_neighborhood_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: base_neighborhood_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.base_neighborhood_id_seq OWNED BY public.base_neighborhood.id;


--
-- Name: block_footprints; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.block_footprints (
    id integer NOT NULL,
    area_m2 double precision,
    "time" integer NOT NULL,
    source character varying(200) NOT NULL,
    colony_id integer,
    locality_id integer,
    municipality_id integer NOT NULL,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: block_footprints_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.block_footprints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: block_footprints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.block_footprints_id_seq OWNED BY public.block_footprints.id;


--
-- Name: blog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog (
    id integer NOT NULL,
    title text NOT NULL,
    image text NOT NULL,
    link text NOT NULL,
    summary text NOT NULL,
    news_date date NOT NULL,
    blog_type integer,
    body text,
    published integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: blog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.blog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: blog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.blog_id_seq OWNED BY public.blog.id;


--
-- Name: building_footprints; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.building_footprints (
    id integer NOT NULL,
    building_code character varying(10) NOT NULL,
    area_m2 double precision,
    "time" integer NOT NULL,
    source character varying(200) NOT NULL,
    neighborhood_id integer,
    locality_id integer,
    municipality_id integer NOT NULL,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: building_footprints_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.building_footprints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: building_footprints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.building_footprints_id_seq OWNED BY public.building_footprints.id;


--
-- Name: business_license_histories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_license_histories (
    id bigint NOT NULL,
    license_folio character varying(255),
    issue_date character varying(255),
    business_line character varying(255),
    detailed_description character varying(255),
    business_line_code character varying(100),
    business_area character varying(255),
    street character varying(100),
    exterior_number character varying(100),
    interior_number character varying(50),
    neighborhood character varying(50),
    cadastral_key character varying(100),
    reference character varying(100),
    coordinate_x character varying(30),
    coordinate_y character varying(30),
    owner_first_name character varying(100),
    owner_last_name_p character varying(100),
    owner_last_name_m character varying(100),
    user_tax_id character varying(25),
    national_id character varying(25),
    owner_phone character varying(25),
    business_name character varying(50),
    owner_email character varying(100),
    owner_street character varying(100),
    owner_exterior_number character varying(100),
    owner_interior_number character varying(50),
    owner_neighborhood character varying(50),
    alcohol_sales character varying(50),
    schedule character varying(100),
    municipality_id integer,
    status integer,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    applicant_first_name character varying(255),
    applicant_last_name_p character varying(255),
    applicant_last_name_m character varying(255),
    applicant_user_tax_id character varying(255),
    applicant_national_id character varying(255),
    applicant_phone character varying(255),
    applicant_street character varying(255),
    applicant_email character varying(255),
    applicant_postal_code character varying(255),
    owner_postal_code character varying(255),
    property_street character varying(255),
    property_neighborhood character varying(255),
    property_interior_number character varying(255),
    property_exterior_number character varying(255),
    property_postal_code character varying(255),
    property_type character varying(255),
    business_trade_name character varying(255),
    investment character varying(255),
    number_of_employees character varying(255),
    number_of_parking_spaces character varying(255),
    license_year character varying(255),
    license_type character varying(255),
    license_status character varying(255),
    reason character varying(255),
    deactivation_status character varying(255),
    payment_status character varying(255),
    opening_time character varying(255),
    closing_time character varying(255),
    alternate_license_year character varying(255),
    payment_user_id integer,
    payment_date timestamp without time zone,
    scanned_pdf character varying(2000),
    step_1 integer,
    step_2 integer,
    step_3 integer,
    step_4 integer,
    minimap_url text,
    reason_file text,
    status_change_date timestamp without time zone
);


--
-- Name: business_license_histories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_license_histories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_license_histories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_license_histories_id_seq OWNED BY public.business_license_histories.id;


--
-- Name: business_licenses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_licenses (
    id bigint NOT NULL,
    owner character varying(200) NOT NULL,
    license_folio character varying(200) NOT NULL,
    commercial_activity character varying(200) NOT NULL,
    industry_classification_code character varying(200) NOT NULL,
    authorized_area character varying(200) NOT NULL,
    opening_time character varying(200) NOT NULL,
    closing_time character varying(200) NOT NULL,
    owner_last_name_p character varying(200),
    owner_last_name_m character varying(200),
    national_id character varying(200),
    owner_profile character varying(200),
    logo_image text,
    signature text,
    minimap_url text,
    scanned_pdf text,
    license_year integer NOT NULL,
    license_category integer,
    generated_by_user_id integer NOT NULL,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    payment_status integer,
    payment_user_id integer,
    deactivation_status integer,
    payment_date timestamp without time zone,
    deactivation_date timestamp without time zone,
    secondary_folio character varying(200),
    deactivation_reason text,
    deactivated_by_user_id integer,
    signer_name_1 character varying(255),
    department_1 character varying(255),
    signature_1 character varying(255),
    signer_name_2 character varying(255),
    department_2 character varying(255),
    signature_2 character varying(255),
    signer_name_3 character varying(255),
    department_3 character varying(255),
    signature_3 character varying(255),
    signer_name_4 character varying(255),
    department_4 character varying(255),
    signature_4 character varying(255),
    license_number integer,
    municipality_id integer,
    license_type character varying(255),
    license_status character varying(255),
    reason character varying(255),
    reason_file text,
    status_change_date timestamp without time zone,
    observations text
);


--
-- Name: business_licenses_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_licenses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_licenses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_licenses_id_seq OWNED BY public.business_licenses.id;


--
-- Name: business_line_configurations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_line_configurations (
    id integer NOT NULL,
    business_line_id integer NOT NULL,
    setting_key character varying(255) NOT NULL,
    setting_value text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: business_line_configurations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_line_configurations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_line_configurations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_line_configurations_id_seq OWNED BY public.business_line_configurations.id;


--
-- Name: business_line_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_line_logs (
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    action character varying(255) NOT NULL,
    previous text,
    user_id integer NOT NULL,
    log_type integer NOT NULL,
    procedure_id integer,
    host character varying(255),
    user_ip character varying(45),
    role_id integer,
    user_agent text,
    post_request text
);


--
-- Name: business_line_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_line_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_line_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_line_logs_id_seq OWNED BY public.business_line_logs.id;


--
-- Name: business_lines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_lines (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: business_lines_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_lines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_lines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_lines_id_seq OWNED BY public.business_lines.id;


--
-- Name: business_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_logs (
    id bigint NOT NULL,
    action character varying(255),
    user_id integer,
    previous_value character varying(1000),
    procedure_id integer,
    host character varying(255),
    user_ip character varying(255),
    post_request character varying(1000),
    device character varying(255),
    log_type integer,
    role_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: business_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_logs_id_seq OWNED BY public.business_logs.id;


--
-- Name: business_sector_certificates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_sector_certificates (
    id bigint NOT NULL,
    business_sector_id integer NOT NULL,
    municipality_id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: business_sector_certificates_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_sector_certificates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_sector_certificates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_sector_certificates_id_seq OWNED BY public.business_sector_certificates.id;


--
-- Name: business_sector_configurations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_sector_configurations (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    business_sector_id integer NOT NULL,
    municipality_id integer NOT NULL,
    inactive_business_flag integer NOT NULL,
    business_impact_flag integer NOT NULL,
    business_sector_certificate_flag integer NOT NULL
);


--
-- Name: business_sector_configurations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_sector_configurations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_sector_configurations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_sector_configurations_id_seq OWNED BY public.business_sector_configurations.id;


--
-- Name: business_sector_impacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_sector_impacts (
    id bigint NOT NULL,
    business_sector_id integer NOT NULL,
    impact integer NOT NULL,
    municipality_id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: business_sector_impacts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_sector_impacts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_sector_impacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_sector_impacts_id_seq OWNED BY public.business_sector_impacts.id;


--
-- Name: business_sectors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_sectors (
    id bigint NOT NULL,
    code character varying(255),
    "SCIAN" character varying(255),
    related_words text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);


--
-- Name: business_sectors_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_sectors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_sectors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_sectors_id_seq OWNED BY public.business_sectors.id;


--
-- Name: business_signatures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_signatures (
    id bigint NOT NULL,
    response json,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    procedure_id integer NOT NULL,
    user_id integer NOT NULL,
    role integer NOT NULL,
    hash_to_sign text,
    signed_hash text
);


--
-- Name: business_signatures_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_signatures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_signatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_signatures_id_seq OWNED BY public.business_signatures.id;


--
-- Name: business_type_configurations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_type_configurations (
    id integer NOT NULL,
    business_type_id integer NOT NULL,
    municipality_id integer NOT NULL,
    is_disabled boolean,
    has_certificate boolean,
    impact_level integer
);


--
-- Name: business_type_configurations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_type_configurations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_type_configurations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_type_configurations_id_seq OWNED BY public.business_type_configurations.id;


--
-- Name: business_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_types (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(500),
    is_active boolean,
    code character varying(50),
    related_words character varying(500)
);


--
-- Name: business_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.business_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: business_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.business_types_id_seq OWNED BY public.business_types.id;


--
-- Name: dependency_resolutions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dependency_resolutions (
    id bigint NOT NULL,
    procedure_id integer NOT NULL,
    role integer,
    user_id integer,
    resolution_status integer,
    resolution_text text,
    resolution_file text,
    signature character varying(255),
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: dependency_resolutions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dependency_resolutions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dependency_resolutions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dependency_resolutions_id_seq OWNED BY public.dependency_resolutions.id;


--
-- Name: dependency_reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dependency_reviews (
    id bigint NOT NULL,
    procedure_id integer NOT NULL,
    municipality_id integer NOT NULL,
    folio character varying(255) NOT NULL,
    role integer NOT NULL,
    start_date timestamp without time zone,
    update_date timestamp without time zone,
    current_status integer,
    current_file text,
    signature character varying(255),
    user_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: dependency_reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dependency_reviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dependency_reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dependency_reviews_id_seq OWNED BY public.dependency_reviews.id;


--
-- Name: dependency_revisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dependency_revisions (
    id integer NOT NULL,
    dependency_id integer NOT NULL,
    revision_notes text,
    revised_at timestamp without time zone DEFAULT now() NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: dependency_revisions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dependency_revisions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dependency_revisions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dependency_revisions_id_seq OWNED BY public.dependency_revisions.id;


--
-- Name: economic_activity_base; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.economic_activity_base (
    id integer NOT NULL,
    name character varying(250) NOT NULL
);


--
-- Name: economic_activity_base_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.economic_activity_base_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: economic_activity_base_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.economic_activity_base_id_seq OWNED BY public.economic_activity_base.id;


--
-- Name: economic_activity_sector; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.economic_activity_sector (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: economic_activity_sector_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.economic_activity_sector_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: economic_activity_sector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.economic_activity_sector_id_seq OWNED BY public.economic_activity_sector.id;


--
-- Name: economic_supports; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.economic_supports (
    id bigint NOT NULL,
    dependency character varying(200),
    scian integer,
    program_name character varying(200),
    url character varying(255),
    program_description text NOT NULL,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: economic_supports_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.economic_supports_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: economic_supports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.economic_supports_id_seq OWNED BY public.economic_supports.id;


--
-- Name: economic_units_directory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.economic_units_directory (
    id integer NOT NULL,
    directory_type character varying(50) NOT NULL,
    commercial_name character varying(150) NOT NULL,
    legal_name character varying(150),
    economic_activity_name character varying(250),
    employed_people character varying(20),
    road_type character varying(40),
    road_name character varying(150),
    road_type_ext_1 character varying(40),
    road_name_ext_1 character varying(150),
    road_type_ext_2 character varying(40),
    road_name_ext_2 character varying(150),
    road_type_ext_3 character varying(40),
    road_name_ext_3 character varying(150),
    exterior_number integer,
    exterior_letter character varying(35),
    building character varying(35),
    building_level character varying(35),
    interior_number integer,
    interior_letter character varying(35),
    settlement_type character varying(35),
    settlement_name character varying(100),
    mall_type character varying(30),
    mall_name character varying(100),
    local_number character varying(35),
    postal_code character varying(5),
    municipality_name character varying(150),
    ageb character varying(4),
    block character varying(4),
    phone character varying(20),
    email character varying(80),
    website character varying(70),
    registration_date character varying(15),
    edited boolean NOT NULL,
    economic_activity_id integer NOT NULL,
    locality_id integer NOT NULL,
    municipality_id integer NOT NULL,
    geom public.geometry(Point,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: economic_units_directory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.economic_units_directory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: economic_units_directory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.economic_units_directory_id_seq OWNED BY public.economic_units_directory.id;


--
-- Name: fields; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fields (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    type character varying(100) NOT NULL,
    description text,
    description_rec text,
    rationale character varying(255),
    options character varying(255),
    options_description character varying(255),
    step integer,
    sequence integer,
    required integer,
    visible_condition character varying(255),
    affected_field character varying(100),
    procedure_type character varying(100),
    dependency_condition character varying(255),
    trade_condition character varying(255),
    status integer,
    municipality_id integer,
    editable integer,
    static_field integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone,
    required_official integer
);


--
-- Name: fields_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.fields_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.fields_id_seq OWNED BY public.fields.id;


--
-- Name: historical_procedures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.historical_procedures (
    id bigint NOT NULL,
    folio character varying(255),
    current_step integer,
    user_signature character varying(255),
    user_id integer,
    window_user_id integer,
    entry_role integer,
    documents_submission_date timestamp without time zone,
    procedure_start_date timestamp without time zone,
    window_seen_date timestamp without time zone,
    license_delivered_date timestamp without time zone,
    has_signature integer,
    no_signature_date timestamp without time zone,
    official_applicant_name character varying(255),
    responsibility_letter character varying(255),
    sent_to_reviewers integer,
    sent_to_reviewers_date timestamp without time zone,
    license_pdf character varying(255),
    payment_order character varying(255),
    status integer NOT NULL,
    step_one integer,
    step_two integer,
    step_three integer,
    step_four integer,
    director_approval integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    window_license_generated integer DEFAULT 0,
    procedure_type character varying(255),
    license_status character varying(255),
    reason character varying(255),
    renewed_folio character varying(255),
    requirements_query_id integer
);


--
-- Name: historical_procedures_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.historical_procedures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: historical_procedures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.historical_procedures_id_seq OWNED BY public.historical_procedures.id;


--
-- Name: inactive_businesses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inactive_businesses (
    id bigint NOT NULL,
    business_line_id integer NOT NULL,
    municipality_id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: inactive_businesses_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.inactive_businesses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: inactive_businesses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.inactive_businesses_id_seq OWNED BY public.inactive_businesses.id;


--
-- Name: issue_resolutions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.issue_resolutions (
    id bigint NOT NULL,
    id_tramite integer NOT NULL,
    rol integer,
    id_usuario integer,
    comentario text,
    comentario_usuario text,
    archivos text,
    fecha_maxima_solventacion timestamp without time zone,
    fecha_ingreso_documentos timestamp without time zone,
    fecha_visto timestamp without time zone,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: issue_resolutions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.issue_resolutions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: issue_resolutions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.issue_resolutions_id_seq OWNED BY public.issue_resolutions.id;


--
-- Name: land_parcel_mapping; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.land_parcel_mapping (
    id integer NOT NULL,
    area_m2 double precision,
    "time" integer NOT NULL,
    source character varying(200) NOT NULL,
    neighborhood_id integer,
    locality_id integer,
    municipality_id integer NOT NULL,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: land_parcel_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.land_parcel_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: land_parcel_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.land_parcel_mapping_id_seq OWNED BY public.land_parcel_mapping.id;


--
-- Name: map_layers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.map_layers (
    id integer NOT NULL,
    value character varying(100) NOT NULL,
    label character varying(180) NOT NULL,
    type character varying(20) NOT NULL,
    url character varying(255) NOT NULL,
    layers character varying(60) NOT NULL,
    visible boolean,
    active boolean,
    attribution character varying(100),
    opacity numeric(3,2),
    server_type character varying(60),
    projection character varying(20),
    version character varying(10),
    format character varying(60) NOT NULL,
    "order" integer,
    editable boolean,
    type_geom character varying(20),
    cql_filter character varying(255)
);


--
-- Name: map_layers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.map_layers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: map_layers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.map_layers_id_seq OWNED BY public.map_layers.id;


--
-- Name: maplayer_municipality; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.maplayer_municipality (
    maplayer_id integer NOT NULL,
    municipality_id bigint NOT NULL
);


--
-- Name: municipalities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.municipalities (
    id bigint NOT NULL,
    name character varying(250) NOT NULL,
    image character varying(250),
    director character varying(250),
    director_signature character varying(250),
    process_sheet integer,
    solving_days integer,
    issue_license integer,
    address character varying(255),
    phone character varying(255),
    responsible_area character varying(250),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone,
    window_license_generation integer,
    license_restrictions text,
    license_price character varying(255),
    initial_folio integer,
    has_zoning boolean
);


--
-- Name: municipalities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.municipalities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: municipalities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.municipalities_id_seq OWNED BY public.municipalities.id;


--
-- Name: municipality_geoms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.municipality_geoms (
    id bigint NOT NULL,
    municipality_id bigint NOT NULL,
    name character varying(250) NOT NULL,
    geom_type character varying(50) NOT NULL,
    coordinates json NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: COLUMN municipality_geoms.municipality_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.municipality_geoms.municipality_id IS 'Associated municipality ID';


--
-- Name: COLUMN municipality_geoms.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.municipality_geoms.name IS 'Municipality name';


--
-- Name: COLUMN municipality_geoms.geom_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.municipality_geoms.geom_type IS 'Geometry type, e.g. ''Polygon''';


--
-- Name: COLUMN municipality_geoms.coordinates; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.municipality_geoms.coordinates IS 'Coordinates in JSON format';


--
-- Name: municipality_geoms_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.municipality_geoms_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: municipality_geoms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.municipality_geoms_id_seq OWNED BY public.municipality_geoms.id;


--
-- Name: municipality_map_layer_base; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.municipality_map_layer_base (
    id bigint NOT NULL,
    map_layer_id integer NOT NULL,
    municipality_id integer NOT NULL
);


--
-- Name: municipality_map_layer_base_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.municipality_map_layer_base_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: municipality_map_layer_base_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.municipality_map_layer_base_id_seq OWNED BY public.municipality_map_layer_base.id;


--
-- Name: municipality_signatures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.municipality_signatures (
    id bigint NOT NULL,
    signer_name character varying(255) NOT NULL,
    department character varying(255) NOT NULL,
    orden integer NOT NULL,
    municipality_id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    signature character varying(255)
);


--
-- Name: municipality_signatures_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.municipality_signatures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: municipality_signatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.municipality_signatures_id_seq OWNED BY public.municipality_signatures.id;


--
-- Name: national_id; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.national_id (
    id integer NOT NULL,
    national_id_number character varying(30),
    national_id_type public.national_id_types,
    user_id integer NOT NULL
);


--
-- Name: national_id_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.national_id_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: national_id_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.national_id_id_seq OWNED BY public.national_id.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id bigint NOT NULL,
    user_id integer,
    applicant_email character varying(100) NOT NULL,
    comment character varying(300),
    file text,
    creation_date timestamp without time zone NOT NULL,
    seen_date timestamp without time zone,
    dependency_file text,
    notified integer,
    notifying_department integer,
    notification_type integer,
    resolution_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    folio character varying(255) NOT NULL
);


--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notifications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: password_recoveries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.password_recoveries (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    token character varying(255) NOT NULL,
    expiration_date timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    used integer DEFAULT 0 NOT NULL
);


--
-- Name: password_recoveries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.password_recoveries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: password_recoveries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.password_recoveries_id_seq OWNED BY public.password_recoveries.id;


--
-- Name: permit_renewals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permit_renewals (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    id_consulta_requisitos integer,
    id_tramite integer
);


--
-- Name: permit_renewals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.permit_renewals_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: permit_renewals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.permit_renewals_id_seq OWNED BY public.permit_renewals.id;


--
-- Name: procedure_registrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.procedure_registrations (
    id integer NOT NULL,
    reference character varying(100),
    area double precision NOT NULL,
    business_sector character varying(150),
    municipality_id integer,
    geom public.geometry(Polygon,32613),
    procedure_type character varying(30),
    procedure_origin character varying(30),
    bbox character varying(200),
    historical_id integer,
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: procedure_registrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.procedure_registrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: procedure_registrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.procedure_registrations_id_seq OWNED BY public.procedure_registrations.id;


--
-- Name: procedures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.procedures (
    id bigint NOT NULL,
    folio character varying(255),
    current_step integer,
    user_signature character varying(255),
    user_id integer,
    window_user_id integer,
    entry_role integer,
    documents_submission_date timestamp without time zone,
    procedure_start_date timestamp without time zone,
    window_seen_date timestamp without time zone,
    license_delivered_date timestamp without time zone,
    has_signature integer,
    no_signature_date timestamp without time zone,
    official_applicant_name character varying(255),
    responsibility_letter character varying(255),
    sent_to_reviewers integer,
    sent_to_reviewers_date timestamp without time zone,
    license_pdf character varying(255),
    payment_order character varying(255),
    status integer NOT NULL,
    step_one integer,
    step_two integer,
    step_three integer,
    step_four integer,
    director_approval integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    window_license_generated integer,
    procedure_type character varying(255),
    license_status character varying(255),
    reason character varying(255),
    renewed_folio character varying(255),
    requirements_query_id integer
);


--
-- Name: procedures_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.procedures_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: procedures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.procedures_id_seq OWNED BY public.procedures.id;


--
-- Name: provisional_openings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.provisional_openings (
    id bigint NOT NULL,
    folio character varying(255) NOT NULL,
    procedure_id integer,
    counter integer,
    granted_by_user_id integer,
    granted_role integer,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    status integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    municipality_id integer,
    created_by integer
);


--
-- Name: provisional_openings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.provisional_openings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: provisional_openings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.provisional_openings_id_seq OWNED BY public.provisional_openings.id;


--
-- Name: public_space_mapping; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.public_space_mapping (
    id integer NOT NULL,
    name character varying(255),
    space_type character varying(40),
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: public_space_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.public_space_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: public_space_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.public_space_mapping_id_seq OWNED BY public.public_space_mapping.id;


--
-- Name: renewal_file_histories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.renewal_file_histories (
    id integer NOT NULL,
    renewal_id integer NOT NULL,
    file_name character varying(255) NOT NULL,
    description text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: renewal_file_histories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.renewal_file_histories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: renewal_file_histories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.renewal_file_histories_id_seq OWNED BY public.renewal_file_histories.id;


--
-- Name: renewal_files; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.renewal_files (
    id bigint NOT NULL,
    file text,
    description text,
    renewal_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: renewal_files_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.renewal_files_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: renewal_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.renewal_files_id_seq OWNED BY public.renewal_files.id;


--
-- Name: renewals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.renewals (
    id integer NOT NULL,
    license_id integer NOT NULL,
    renewal_date timestamp without time zone NOT NULL,
    status character varying(50),
    observations text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: renewals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.renewals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: renewals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.renewals_id_seq OWNED BY public.renewals.id;


--
-- Name: requirements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.requirements (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    municipality_id integer NOT NULL,
    field_id integer NOT NULL,
    requirement_code character varying(300)
);


--
-- Name: requirements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.requirements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: requirements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.requirements_id_seq OWNED BY public.requirements.id;


--
-- Name: requirements_querys; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.requirements_querys (
    id bigint NOT NULL,
    folio character varying(255),
    street character varying(100) NOT NULL,
    neighborhood character varying(100) NOT NULL,
    municipality_name character varying(50) NOT NULL,
    municipality_id integer NOT NULL,
    scian_code character varying(100) NOT NULL,
    scian_name character varying(100) NOT NULL,
    property_area numeric(8,2) NOT NULL,
    activity_area numeric(8,2) NOT NULL,
    applicant_name character varying(100),
    applicant_character character varying(100),
    person_type character varying(100),
    minimap_url text,
    restrictions json,
    status integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    year_folio integer NOT NULL,
    alcohol_sales integer NOT NULL,
    primary_folio character varying(255)
);


--
-- Name: requirements_querys_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.requirements_querys_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: requirements_querys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.requirements_querys_id_seq OWNED BY public.requirements_querys.id;


--
-- Name: reviewers_chat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reviewers_chat (
    id bigint NOT NULL,
    id_tramite integer NOT NULL,
    ir_usuario integer NOT NULL,
    rol integer,
    comentario text,
    imagen text,
    archivo_adjunto character varying(255),
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: reviewers_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reviewers_chat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reviewers_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reviewers_chat_id_seq OWNED BY public.reviewers_chat.id;


--
-- Name: sub_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sub_roles (
    id bigint NOT NULL,
    name character varying(250) NOT NULL,
    description character varying(250) NOT NULL,
    municipality_id integer,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: sub_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sub_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sub_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sub_roles_id_seq OWNED BY public.sub_roles.id;


--
-- Name: technical_sheet_downloads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.technical_sheet_downloads (
    id bigint NOT NULL,
    city character varying(255),
    email character varying(255),
    age character varying(255),
    name character varying(255),
    sector character varying(255),
    uses text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    municipality_id integer NOT NULL,
    address character varying(255)
);


--
-- Name: technical_sheet_downloads_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.technical_sheet_downloads_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: technical_sheet_downloads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.technical_sheet_downloads_id_seq OWNED BY public.technical_sheet_downloads.id;


--
-- Name: technical_sheets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.technical_sheets (
    id bigint NOT NULL,
    uuid character varying(255) NOT NULL,
    address text NOT NULL,
    square_meters text NOT NULL,
    coordinates text NOT NULL,
    image text NOT NULL,
    municipality_id integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    technical_sheet_download_id integer
);


--
-- Name: technical_sheets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.technical_sheets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: technical_sheets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.technical_sheets_id_seq OWNED BY public.technical_sheets.id;


--
-- Name: urban_development_zonings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.urban_development_zonings (
    id integer NOT NULL,
    district character varying(120) NOT NULL,
    sub_district character varying(18),
    publication_date date,
    primary_area_classification_key character varying(50),
    primary_area_classification_description character varying(255),
    secondary_area_classification_key character varying(50),
    secondary_area_classification_description character varying(255),
    land_use_key character varying(50),
    primary_zone_classification_key character varying(255),
    primary_zone_classification_description character varying(255),
    secondary_zone_classification_key character varying(255),
    secondary_zone_classification_description character varying(255),
    area_classification_number character varying(50),
    zone_classification_number character varying(50),
    zoning_key character varying(160),
    restriction character varying(250),
    "user" character varying(60),
    "timestamp" timestamp with time zone,
    aux character varying(50),
    municipality_id integer NOT NULL,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: urban_development_zonings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.urban_development_zonings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: urban_development_zonings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.urban_development_zonings_id_seq OWNED BY public.urban_development_zonings.id;


--
-- Name: urban_development_zonings_standard; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.urban_development_zonings_standard (
    id integer NOT NULL,
    district character varying(120) NOT NULL,
    sub_district character varying(8),
    publication_date date,
    primary_area_classification_key character varying(120),
    primary_area_classification_description character varying(255),
    secondary_area_classification_key character varying(120),
    secondary_area_classification_description character varying(255),
    primary_zone_classification_key character varying(255),
    primary_zone_classification_description character varying(255),
    secondary_zone_classification_key character varying(255),
    secondary_zone_classification_description character varying(255),
    area_classification_number character varying(150),
    zone_classification_number character varying(150),
    zoning_key character varying(255),
    restriction character varying(255),
    municipality_id integer NOT NULL,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: urban_development_zonings_standard_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.urban_development_zonings_standard_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: urban_development_zonings_standard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.urban_development_zonings_standard_id_seq OWNED BY public.urban_development_zonings_standard.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles (
    id bigint NOT NULL,
    name character varying(20) NOT NULL,
    description character varying(200),
    municipality_id integer,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: user_roles_assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles_assignments (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    user_id bigint NOT NULL,
    role_id bigint,
    pending_role_id integer,
    role_status character varying(20),
    token character varying(36)
);


--
-- Name: user_roles_assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_roles_assignments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_roles_assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_roles_assignments_id_seq OWNED BY public.user_roles_assignments.id;


--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- Name: user_tax_id; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_tax_id (
    id integer NOT NULL,
    tax_id_number character varying(50),
    tax_id_type public.tax_id_types,
    user_id integer NOT NULL
);


--
-- Name: user_tax_id_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_tax_id_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_tax_id_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_tax_id_id_seq OWNED BY public.user_tax_id.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    api_token character varying(100),
    api_token_expiration timestamp without time zone,
    subrole_id integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone,
    role_id bigint,
    is_active boolean NOT NULL,
    paternal_last_name character varying(50) NOT NULL,
    maternal_last_name character varying(50),
    user_tax_id character varying(50),
    cellphone character varying(50) NOT NULL,
    municipality_id integer,
    national_id character varying(50),
    username character varying(150),
    is_staff boolean DEFAULT false NOT NULL,
    is_superuser boolean DEFAULT false NOT NULL,
    last_login timestamp with time zone,
    date_joined timestamp with time zone
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: water_body_footprints; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.water_body_footprints (
    id integer NOT NULL,
    area_m2 double precision,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: water_body_footprints_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.water_body_footprints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: water_body_footprints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.water_body_footprints_id_seq OWNED BY public.water_body_footprints.id;


--
-- Name: zoning_control_regulations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.zoning_control_regulations (
    id integer NOT NULL,
    district character varying(2) NOT NULL,
    regulation_key character varying(160) NOT NULL,
    land_use character varying(200) NOT NULL,
    density character varying(190),
    intensity character varying(190),
    business_sector character varying(255),
    minimum_area character varying(190),
    minimum_frontage character varying(190),
    building_index character varying(190),
    land_occupation_coefficient character varying(190),
    land_utilization_coefficient character varying(190),
    max_building_height character varying(190),
    parking_spaces character varying(190),
    front_gardening_percentage character varying(190),
    front_restriction character varying(190),
    lateral_restrictions character varying(190),
    rear_restriction character varying(190),
    building_mode character varying(190),
    observations text,
    municipality_id integer NOT NULL,
    urban_environmental_value_areas boolean NOT NULL,
    planned_public_space boolean NOT NULL,
    increase_land_utilization_coefficient character varying(190),
    hotel_occupation_index character varying(160)
);


--
-- Name: zoning_control_regulations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.zoning_control_regulations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: zoning_control_regulations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.zoning_control_regulations_id_seq OWNED BY public.zoning_control_regulations.id;


--
-- Name: zoning_impact_level; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.zoning_impact_level (
    id integer NOT NULL,
    impact_level integer NOT NULL,
    municipality_id integer NOT NULL,
    geom public.geometry(Polygon,32613),
    CONSTRAINT enforce_dims_geom CHECK ((public.st_ndims(geom) = 2)),
    CONSTRAINT enforce_geotype_geom CHECK (((public.geometrytype(geom) = 'POLYGON'::text) OR (geom IS NULL))),
    CONSTRAINT enforce_srid_geom CHECK ((public.st_srid(geom) = 32613))
);


--
-- Name: zoning_impact_level_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.zoning_impact_level_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: zoning_impact_level_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.zoning_impact_level_id_seq OWNED BY public.zoning_impact_level.id;


--
-- Name: answers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers ALTER COLUMN id SET DEFAULT nextval('public.answers_id_seq'::regclass);


--
-- Name: answers_json id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers_json ALTER COLUMN id SET DEFAULT nextval('public.answers_json_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: base_administrative_division id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_administrative_division ALTER COLUMN id SET DEFAULT nextval('public.base_administrative_division_id_seq'::regclass);


--
-- Name: base_locality id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_locality ALTER COLUMN id SET DEFAULT nextval('public.base_locality_id_seq'::regclass);


--
-- Name: base_map_layer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_map_layer ALTER COLUMN id SET DEFAULT nextval('public.base_map_layer_id_seq'::regclass);


--
-- Name: base_municipality id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_municipality ALTER COLUMN id SET DEFAULT nextval('public.base_municipality_id_seq'::regclass);


--
-- Name: base_neighborhood id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_neighborhood ALTER COLUMN id SET DEFAULT nextval('public.base_neighborhood_id_seq'::regclass);


--
-- Name: block_footprints id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.block_footprints ALTER COLUMN id SET DEFAULT nextval('public.block_footprints_id_seq'::regclass);


--
-- Name: blog id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog ALTER COLUMN id SET DEFAULT nextval('public.blog_id_seq'::regclass);


--
-- Name: building_footprints id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_footprints ALTER COLUMN id SET DEFAULT nextval('public.building_footprints_id_seq'::regclass);


--
-- Name: business_license_histories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_license_histories ALTER COLUMN id SET DEFAULT nextval('public.business_license_histories_id_seq'::regclass);


--
-- Name: business_licenses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_licenses ALTER COLUMN id SET DEFAULT nextval('public.business_licenses_id_seq'::regclass);


--
-- Name: business_line_configurations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_line_configurations ALTER COLUMN id SET DEFAULT nextval('public.business_line_configurations_id_seq'::regclass);


--
-- Name: business_line_logs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_line_logs ALTER COLUMN id SET DEFAULT nextval('public.business_line_logs_id_seq'::regclass);


--
-- Name: business_lines id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_lines ALTER COLUMN id SET DEFAULT nextval('public.business_lines_id_seq'::regclass);


--
-- Name: business_logs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_logs ALTER COLUMN id SET DEFAULT nextval('public.business_logs_id_seq'::regclass);


--
-- Name: business_sector_certificates id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_certificates ALTER COLUMN id SET DEFAULT nextval('public.business_sector_certificates_id_seq'::regclass);


--
-- Name: business_sector_configurations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_configurations ALTER COLUMN id SET DEFAULT nextval('public.business_sector_configurations_id_seq'::regclass);


--
-- Name: business_sector_impacts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_impacts ALTER COLUMN id SET DEFAULT nextval('public.business_sector_impacts_id_seq'::regclass);


--
-- Name: business_sectors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sectors ALTER COLUMN id SET DEFAULT nextval('public.business_sectors_id_seq'::regclass);


--
-- Name: business_signatures id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_signatures ALTER COLUMN id SET DEFAULT nextval('public.business_signatures_id_seq'::regclass);


--
-- Name: business_type_configurations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_type_configurations ALTER COLUMN id SET DEFAULT nextval('public.business_type_configurations_id_seq'::regclass);


--
-- Name: business_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_types ALTER COLUMN id SET DEFAULT nextval('public.business_types_id_seq'::regclass);


--
-- Name: dependency_resolutions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_resolutions ALTER COLUMN id SET DEFAULT nextval('public.dependency_resolutions_id_seq'::regclass);


--
-- Name: dependency_reviews id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_reviews ALTER COLUMN id SET DEFAULT nextval('public.dependency_reviews_id_seq'::regclass);


--
-- Name: dependency_revisions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_revisions ALTER COLUMN id SET DEFAULT nextval('public.dependency_revisions_id_seq'::regclass);


--
-- Name: economic_activity_base id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_activity_base ALTER COLUMN id SET DEFAULT nextval('public.economic_activity_base_id_seq'::regclass);


--
-- Name: economic_activity_sector id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_activity_sector ALTER COLUMN id SET DEFAULT nextval('public.economic_activity_sector_id_seq'::regclass);


--
-- Name: economic_supports id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_supports ALTER COLUMN id SET DEFAULT nextval('public.economic_supports_id_seq'::regclass);


--
-- Name: economic_units_directory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_units_directory ALTER COLUMN id SET DEFAULT nextval('public.economic_units_directory_id_seq'::regclass);


--
-- Name: fields id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fields ALTER COLUMN id SET DEFAULT nextval('public.fields_id_seq'::regclass);


--
-- Name: historical_procedures id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historical_procedures ALTER COLUMN id SET DEFAULT nextval('public.historical_procedures_id_seq'::regclass);


--
-- Name: inactive_businesses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inactive_businesses ALTER COLUMN id SET DEFAULT nextval('public.inactive_businesses_id_seq'::regclass);


--
-- Name: issue_resolutions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_resolutions ALTER COLUMN id SET DEFAULT nextval('public.issue_resolutions_id_seq'::regclass);


--
-- Name: land_parcel_mapping id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.land_parcel_mapping ALTER COLUMN id SET DEFAULT nextval('public.land_parcel_mapping_id_seq'::regclass);


--
-- Name: map_layers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.map_layers ALTER COLUMN id SET DEFAULT nextval('public.map_layers_id_seq'::regclass);


--
-- Name: municipalities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipalities ALTER COLUMN id SET DEFAULT nextval('public.municipalities_id_seq'::regclass);


--
-- Name: municipality_geoms id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_geoms ALTER COLUMN id SET DEFAULT nextval('public.municipality_geoms_id_seq'::regclass);


--
-- Name: municipality_map_layer_base id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_map_layer_base ALTER COLUMN id SET DEFAULT nextval('public.municipality_map_layer_base_id_seq'::regclass);


--
-- Name: municipality_signatures id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_signatures ALTER COLUMN id SET DEFAULT nextval('public.municipality_signatures_id_seq'::regclass);


--
-- Name: national_id id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.national_id ALTER COLUMN id SET DEFAULT nextval('public.national_id_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: password_recoveries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_recoveries ALTER COLUMN id SET DEFAULT nextval('public.password_recoveries_id_seq'::regclass);


--
-- Name: permit_renewals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permit_renewals ALTER COLUMN id SET DEFAULT nextval('public.permit_renewals_id_seq'::regclass);


--
-- Name: procedure_registrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedure_registrations ALTER COLUMN id SET DEFAULT nextval('public.procedure_registrations_id_seq'::regclass);


--
-- Name: procedures id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedures ALTER COLUMN id SET DEFAULT nextval('public.procedures_id_seq'::regclass);


--
-- Name: provisional_openings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.provisional_openings ALTER COLUMN id SET DEFAULT nextval('public.provisional_openings_id_seq'::regclass);


--
-- Name: public_space_mapping id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.public_space_mapping ALTER COLUMN id SET DEFAULT nextval('public.public_space_mapping_id_seq'::regclass);


--
-- Name: renewal_file_histories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renewal_file_histories ALTER COLUMN id SET DEFAULT nextval('public.renewal_file_histories_id_seq'::regclass);


--
-- Name: renewal_files id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renewal_files ALTER COLUMN id SET DEFAULT nextval('public.renewal_files_id_seq'::regclass);


--
-- Name: renewals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renewals ALTER COLUMN id SET DEFAULT nextval('public.renewals_id_seq'::regclass);


--
-- Name: requirements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements ALTER COLUMN id SET DEFAULT nextval('public.requirements_id_seq'::regclass);


--
-- Name: requirements_querys id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements_querys ALTER COLUMN id SET DEFAULT nextval('public.requirements_querys_id_seq'::regclass);


--
-- Name: reviewers_chat id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviewers_chat ALTER COLUMN id SET DEFAULT nextval('public.reviewers_chat_id_seq'::regclass);


--
-- Name: sub_roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sub_roles ALTER COLUMN id SET DEFAULT nextval('public.sub_roles_id_seq'::regclass);


--
-- Name: technical_sheet_downloads id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technical_sheet_downloads ALTER COLUMN id SET DEFAULT nextval('public.technical_sheet_downloads_id_seq'::regclass);


--
-- Name: technical_sheets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technical_sheets ALTER COLUMN id SET DEFAULT nextval('public.technical_sheets_id_seq'::regclass);


--
-- Name: urban_development_zonings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.urban_development_zonings ALTER COLUMN id SET DEFAULT nextval('public.urban_development_zonings_id_seq'::regclass);


--
-- Name: urban_development_zonings_standard id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.urban_development_zonings_standard ALTER COLUMN id SET DEFAULT nextval('public.urban_development_zonings_standard_id_seq'::regclass);


--
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- Name: user_roles_assignments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles_assignments ALTER COLUMN id SET DEFAULT nextval('public.user_roles_assignments_id_seq'::regclass);


--
-- Name: user_tax_id id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_tax_id ALTER COLUMN id SET DEFAULT nextval('public.user_tax_id_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: water_body_footprints id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.water_body_footprints ALTER COLUMN id SET DEFAULT nextval('public.water_body_footprints_id_seq'::regclass);


--
-- Name: zoning_control_regulations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zoning_control_regulations ALTER COLUMN id SET DEFAULT nextval('public.zoning_control_regulations_id_seq'::regclass);


--
-- Name: zoning_impact_level id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zoning_impact_level ALTER COLUMN id SET DEFAULT nextval('public.zoning_impact_level_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
fd20e65ab5e6
\.


--
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.answers (id, procedure_id, name, value, user_id, status, created_at, updated_at, deleted_at) FROM stdin;
17	28	construction_type	residential	1	1	\N	\N	\N
18	28	area_sq_meters	250	1	1	\N	\N	\N
19	28	floors_number	2	1	1	\N	\N	\N
20	28	parking_spaces	2	1	1	\N	\N	\N
21	29	business_name	Café La Esquina	2	1	\N	\N	\N
22	29	business_type	restaurant	2	1	\N	\N	\N
23	29	employee_count	12	2	1	\N	\N	\N
24	29	has_liquor_license	true	2	1	\N	\N	\N
25	30	business_name	Café La Esquina	2	1	\N	\N	\N
26	30	business_type	restaurant	2	1	\N	\N	\N
27	30	employee_count	15	2	1	\N	\N	\N
28	30	has_liquor_license	true	2	1	\N	\N	\N
29	31	construction_type	commercial	3	1	\N	\N	\N
30	31	area_sq_meters	450	3	1	\N	\N	\N
31	31	floors_number	3	3	1	\N	\N	\N
32	31	parking_spaces	8	3	1	\N	\N	\N
\.


--
-- Data for Name: answers_json; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.answers_json (id, procedure_id, user_id, answers, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
\.


--
-- Data for Name: base_administrative_division; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.base_administrative_division (id, name, code, division_type, geom) FROM stdin;
\.


--
-- Data for Name: base_locality; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.base_locality (id, name, scope, municipality_code, locality_code, geocode, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: base_map_layer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.base_map_layer (id, value, label, type, url, layers, visible, active, attribution, opacity, server_type, projection, version, format, "order", editable, type_geom, cql_filter) FROM stdin;
\.


--
-- Data for Name: base_municipality; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.base_municipality (id, municipality_id, name, entity_code, municipality_code, geocode, has_zoning, geom) FROM stdin;
\.


--
-- Data for Name: base_neighborhood; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.base_neighborhood (id, name, postal_code, locality_id, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: block_footprints; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.block_footprints (id, area_m2, "time", source, colony_id, locality_id, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: blog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog (id, title, image, link, summary, news_date, blog_type, body, published, created_at, updated_at) FROM stdin;
1	Urban Planning Launch	https://example.com/image1.jpg	https://visorurbano.com/blog/urban-planning	A new initiative for sustainable urban planning.	2023-10-10	1	Full article content about the launch of a new urban planning program.	1	2025-04-14 10:21:37.767259	2025-04-14 10:21:37.767259
2	Citizen Participation Guide	https://example.com/image2.jpg	https://visorurbano.com/blog/citizen-guide	How to get involved in municipal decisions.	2023-10-15	2	Details on how citizens can engage with their local government.	1	2025-04-14 10:21:37.767259	2025-04-14 10:21:37.767259
3	Internal Process Optimization	https://example.com/image3.jpg	https://visorurbano.com/blog/internal-process	Behind-the-scenes improvements to digital services.	2023-09-30	3	Technical deep dive into the new back-office features.	0	2025-04-14 10:21:37.767259	2025-04-14 10:21:37.767259
4	Public Survey Results	https://example.com/image4.jpg	https://visorurbano.com/blog/survey-results	Summary of key insights from recent citizen surveys.	2023-11-01	1	Survey analysis for policy improvement.	1	2025-04-14 10:21:37.767259	2025-04-14 10:21:37.767259
5	Upcoming Urban Projects	https://example.com/image5.jpg	https://visorurbano.com/blog/2024-projects	What to expect in 2024.	2024-01-05	2	Pipeline of urban projects planned for the next year.	0	2025-04-14 10:21:37.767259	2025-04-14 10:21:37.767259
6	string	string	string	string	2025-04-14	0	string	0	\N	\N
\.


--
-- Data for Name: building_footprints; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.building_footprints (id, building_code, area_m2, "time", source, neighborhood_id, locality_id, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: business_license_histories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_license_histories (id, license_folio, issue_date, business_line, detailed_description, business_line_code, business_area, street, exterior_number, interior_number, neighborhood, cadastral_key, reference, coordinate_x, coordinate_y, owner_first_name, owner_last_name_p, owner_last_name_m, user_tax_id, national_id, owner_phone, business_name, owner_email, owner_street, owner_exterior_number, owner_interior_number, owner_neighborhood, alcohol_sales, schedule, municipality_id, status, deleted_at, created_at, updated_at, applicant_first_name, applicant_last_name_p, applicant_last_name_m, applicant_user_tax_id, applicant_national_id, applicant_phone, applicant_street, applicant_email, applicant_postal_code, owner_postal_code, property_street, property_neighborhood, property_interior_number, property_exterior_number, property_postal_code, property_type, business_trade_name, investment, number_of_employees, number_of_parking_spaces, license_year, license_type, license_status, reason, deactivation_status, payment_status, opening_time, closing_time, alternate_license_year, payment_user_id, payment_date, scanned_pdf, step_1, step_2, step_3, step_4, minimap_url, reason_file, status_change_date) FROM stdin;
1	LIC-2024-001	2024-01-15	Restaurante	Servicio de alimentos y bebidas	REST-001	Zona Centro	Av. Juárez	123	A	Centro	CAD-001-2024	Frente a la plaza principal	19.4326	-99.1332	Juan Carlos	García	López	GALO800815ABC	GALO800815HDFMRN01	555-0101	Restaurante El Buen Sabor	juan.garcia@email.com	Calle Morelos	456	2	Roma Norte	Sí	Lunes a Domingo 8:00-22:00	1	1	\N	2025-05-29 09:53:42.015547	2025-05-29 09:53:42.015547	María Elena	Hernández	Ruiz	HERM850920XYZ	HERM850920MDFRNR08	555-0102	Calle Reforma	maria.hernandez@email.com	06700	11000	Av. Juárez	Centro	A	123	06000	Local comercial	El Buen Sabor S.A. de C.V.	500000	15	5	2024	Comercial	Activa	\N	\N	Pagado	08:00	22:00	2024	1	2024-01-20 10:30:00	\N	1	1	1	1	\N	\N	\N
2	LIC-2024-002	2024-02-10	Farmacia	Venta de medicamentos y productos farmacéuticos	FARM-002	Zona Residencial	Calle Hidalgo	789	\N	Las Flores	CAD-002-2024	Esquina con Av. Independencia	19.4285	-99.1276	Ana Patricia	Martínez	Sánchez	MASA751201DEF	MASA751201MDFRNN02	555-0201	Farmacia San Rafael	ana.martinez@email.com	Calle Revolución	321	\N	Doctores	No	Lunes a Sábado 7:00-21:00	1	1	\N	2025-05-29 09:53:42.015547	2025-05-29 09:53:42.015547	Roberto	Jiménez	Castro	JICR800515GHI	JICR800515HDFMBT05	555-0202	Av. Universidad	roberto.jimenez@email.com	03100	06760	Calle Hidalgo	Las Flores	\N	789	03000	Local comercial	Farmacia San Rafael S.C.	300000	8	3	2024	Comercial	Activa	\N	\N	Pagado	07:00	21:00	2024	2	2024-02-15 14:15:00	\N	1	1	1	0	\N	\N	\N
3	LIC-2024-003	2024-03-05	Abarrotes	Venta de productos de primera necesidad	ABAR-003	Zona Popular	Calle Aldama	456	B	San Juan	CAD-003-2024	A media cuadra del mercado	19.4240	-99.1420	Luis Fernando	Rodríguez	Morales	ROML690830JKL	ROML690830HDFDRR03	555-0301	Abarrotes La Esquina	luis.rodriguez@email.com	Calle Allende	654	1	Guerrero	Sí	Todos los días 6:00-23:00	2	1	\N	2025-05-29 09:53:42.015547	2025-05-29 09:53:42.015547	Carmen	López	Vega	LOVC901012MNO	LOVC901012MDFPGR06	555-0302	Calle Mina	carmen.lopez@email.com	06300	06050	Calle Aldama	San Juan	B	456	06200	Local comercial	Abarrotes La Esquina	150000	5	2	2024	Comercial	Activa	\N	\N	Pagado	06:00	23:00	2024	3	2024-03-10 09:45:00	\N	1	1	0	0	\N	\N	\N
4	LIC-2024-004	2024-04-12	Estética	Servicios de belleza y cuidado personal	EST-004	Zona Comercial	Av. Insurgentes	1001	3	Condesa	CAD-004-2024	Plaza comercial nivel 2	19.4120	-99.1700	Sofía	Mendoza	Ramírez	MERS840607PQR	MERS840607MDFNMF04	555-0401	Estética Bella Vista	sofia.mendoza@email.com	Calle Amsterdam	78	4	Hipódromo	No	Martes a Domingo 9:00-19:00	1	1	\N	2025-05-29 09:53:42.015547	2025-05-29 09:53:42.015547	Diego	Vargas	Herrera	VAHD770925STU	VAHD770925HDFRRG07	555-0402	Av. Chapultepec	diego.vargas@email.com	06140	11560	Av. Insurgentes	Condesa	3	1001	06100	Local en plaza	Bella Vista Estética S.A.	200000	6	0	2024	Servicios	Pendiente	Documentación incompleta	\N	Pendiente	09:00	19:00	2024	4	\N	\N	1	1	0	0	\N	\N	\N
6	LIC-2023-099	2023-12-01	Panadería	Elaboración y venta de productos de panadería	PAN-099	Zona Centro	Calle Madero	99	\N	Centro Histórico	CAD-099-2023	Cerca del zócalo	19.4338	-99.1370	Fernando	Gutiérrez	Silva	GUSF650101BCD	GUSF650101HDFLLR10	555-0099	Panadería Tradicional	fernando.gutierrez@email.com	Calle 16 de Septiembre	88	\N	Centro	No	Martes a Domingo 6:00-20:00	1	0	\N	2025-05-29 09:53:42.015547	2025-05-29 09:53:42.015547	Rosa María	Castillo	Núñez	CANR720815EFG	CANR720815MDFSTR11	555-0098	Calle 5 de Mayo	rosa.castillo@email.com	06000	06010	Calle Madero	Centro Histórico	\N	99	06000	Local comercial	Panadería Tradicional	120000	4	1	2023	Comercial	Cancelada	Cierre del negocio	Cancelada por solicitud del propietario	Cancelado	06:00	20:00	2023	6	2023-12-15 16:30:00	\N	1	1	1	1	\N	\N	\N
5	LIC-2024-005	2024-05-08	Taller Mecánico	Reparación y mantenimiento automotriz	TALL-005	Zona Industrial	Calle Taller	200	\N	Industrial	CAD-005-2024	Zona de talleres	19.3850	-99.1580	Miguel Ángel	Torres	Guerrero	TOGM820403VWX	TOGM820403HDFRRG08	555-0501	Taller Automotriz El Rayo	miguel.torres@email.com	Calle Industria	567	\N	Obrera	No	Lunes a Viernes 8:00-18:00	2	1	\N	2025-05-29 09:53:42.015547	2025-05-29 09:53:42.015547	Leticia	Flores	Díaz	FODL880212YZA	FODL880212MDFLLR09	555-0502	Av. Trabajo	leticia.flores@email.com	03400	08100	Calle Taller	Industrial	\N	200	03300	Nave industrial	Automotriz El Rayo S.A.	800000	12	15	2024	Industrial	Activa	\N	\N	Pagado	08:00	18:00	2024	1	2024-05-15 11:20:00	\N	1	1	1	1	\N	\N	\N
\.


--
-- Data for Name: business_licenses; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_licenses (id, owner, license_folio, commercial_activity, industry_classification_code, authorized_area, opening_time, closing_time, owner_last_name_p, owner_last_name_m, national_id, owner_profile, logo_image, signature, minimap_url, scanned_pdf, license_year, license_category, generated_by_user_id, deleted_at, created_at, updated_at, payment_status, payment_user_id, deactivation_status, payment_date, deactivation_date, secondary_folio, deactivation_reason, deactivated_by_user_id, signer_name_1, department_1, signature_1, signer_name_2, department_2, signature_2, signer_name_3, department_3, signature_3, signer_name_4, department_4, signature_4, license_number, municipality_id, license_type, license_status, reason, reason_file, status_change_date, observations) FROM stdin;
\.


--
-- Data for Name: business_line_configurations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_line_configurations (id, business_line_id, setting_key, setting_value, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: business_line_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_line_logs (id, created_at, updated_at, action, previous, user_id, log_type, procedure_id, host, user_ip, role_id, user_agent, post_request) FROM stdin;
\.


--
-- Data for Name: business_lines; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_lines (id, name, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: business_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_logs (id, action, user_id, previous_value, procedure_id, host, user_ip, post_request, device, log_type, role_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: business_sector_certificates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_sector_certificates (id, business_sector_id, municipality_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: business_sector_configurations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_sector_configurations (id, created_at, updated_at, business_sector_id, municipality_id, inactive_business_flag, business_impact_flag, business_sector_certificate_flag) FROM stdin;
\.


--
-- Data for Name: business_sector_impacts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_sector_impacts (id, business_sector_id, impact, municipality_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: business_sectors; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_sectors (id, code, "SCIAN", related_words, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: business_signatures; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_signatures (id, response, deleted_at, created_at, updated_at, procedure_id, user_id, role, hash_to_sign, signed_hash) FROM stdin;
1	{"signed_hash": "1BJ0GlY8q2Yf9/ofP0A+t5x+FJq+WgVLiXkRmYEmW7A=", "generated_at": "2025-05-31T13:17:33.996613", "curp": "ABCD123456HDFRRL09", "procedure_id": 3, "procedure_part": "business_license_application", "cert_filename": "certificate_1.cer", "key_filename": "private_key_1.key", "signature_type": "business_license_application", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.996618	2025-05-31 13:17:33.996618	3	1	1	chain_comercial_license_data_to_sign	1BJ0GlY8q2Yf9/ofP0A+t5x+FJq+WgVLiXkRmYEmW7A=
2	{"signed_hash": "dLbnVRAMP56woTF4U58gqFn5cSMQID0XzEcDWpny4yE=", "generated_at": "2025-05-31T13:17:33.996625", "curp": "XYZW654321MDFGGR08", "procedure_id": 1, "procedure_part": "permit_renewal", "cert_filename": "certificate_2.cer", "key_filename": "private_key_2.key", "signature_type": "permit_renewal", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.996628	2025-05-31 13:17:33.996628	1	2	1	chain_industrial_permit_data_to_sign	dLbnVRAMP56woTF4U58gqFn5cSMQID0XzEcDWpny4yE=
3	{"signed_hash": "PX0VtomuLJu7gD5GDXb7yhOKtZxu6j1K3rSiIvRekpI=", "generated_at": "2025-05-31T13:17:33.996632", "curp": "JUAN850315HDFRNT02", "procedure_id": 2, "procedure_part": "license_modification", "cert_filename": "certificate_3.cer", "key_filename": "private_key_3.key", "signature_type": "license_modification", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.996634	2025-05-31 13:17:33.996635	2	3	1	chain_restaurant_license_data_to_sign	PX0VtomuLJu7gD5GDXb7yhOKtZxu6j1K3rSiIvRekpI=
4	{"signed_hash": "p7HVfE6ScViyA53rTx5wjRkzuW6sbHKYyNaW3Vd/EuM=", "generated_at": "2025-05-31T13:17:33.996638", "curp": "MARIA900420MDFRMR05", "procedure_id": 4, "procedure_part": "regulatory_compliance", "cert_filename": "certificate_4.cer", "key_filename": "private_key_4.key", "signature_type": "regulatory_compliance", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.99664	2025-05-31 13:17:33.99664	4	1	1	chain_retail_permit_data_to_sign	p7HVfE6ScViyA53rTx5wjRkzuW6sbHKYyNaW3Vd/EuM=
5	{"signed_hash": "L2fjgkG7GAC15vkO4A746oZqJVA19orD0jdHROWDDM4=", "generated_at": "2025-05-31T13:17:33.996643", "curp": "CARLOS751010HDFRRL01", "procedure_id": 5, "procedure_part": "inspection_certification", "cert_filename": "certificate_5.cer", "key_filename": "private_key_5.key", "signature_type": "inspection_certification", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.996645	2025-05-31 13:17:33.996645	5	2	1	chain_service_license_data_to_sign	L2fjgkG7GAC15vkO4A746oZqJVA19orD0jdHROWDDM4=
6	{"signed_hash": "xME9xC3PJlH3M4nL5gA4upPpCqMghsZUokLDwGk/rvc=", "generated_at": "2025-05-31T13:17:33.996648", "curp": "ABCD123456HDFRRL09", "procedure_id": 3, "procedure_part": "business_license_application", "cert_filename": "certificate_6.cer", "key_filename": "private_key_6.key", "signature_type": "business_license_application", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.99665	2025-05-31 13:17:33.996651	3	3	1	chain_comercial_license_data_to_sign	xME9xC3PJlH3M4nL5gA4upPpCqMghsZUokLDwGk/rvc=
7	{"signed_hash": "EbSCI9LH6jvmUUCapKsiLQtIy0mzUr+bWo1ex0gc/es=", "generated_at": "2025-05-31T13:17:33.996654", "curp": "XYZW654321MDFGGR08", "procedure_id": 1, "procedure_part": "permit_renewal", "cert_filename": "certificate_7.cer", "key_filename": "private_key_7.key", "signature_type": "permit_renewal", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.996655	2025-05-31 13:17:33.996656	1	1	1	chain_industrial_permit_data_to_sign	EbSCI9LH6jvmUUCapKsiLQtIy0mzUr+bWo1ex0gc/es=
8	{"signed_hash": "iywFXtDi6RP7AxBgpZqRBL+uaiHumGBeEx9aiZ6gFHM=", "generated_at": "2025-05-31T13:17:33.996658", "curp": "JUAN850315HDFRNT02", "procedure_id": 2, "procedure_part": "license_modification", "cert_filename": "certificate_8.cer", "key_filename": "private_key_8.key", "signature_type": "license_modification", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.99666	2025-05-31 13:17:33.99666	2	2	1	chain_restaurant_license_data_to_sign	iywFXtDi6RP7AxBgpZqRBL+uaiHumGBeEx9aiZ6gFHM=
9	{"signed_hash": "SveqoJ+Mh4ERS64i2B48U9nHJ3Y8G28HJStbTtMEzeY=", "generated_at": "2025-05-31T13:17:33.996663", "curp": "MARIA900420MDFRMR05", "procedure_id": 4, "procedure_part": "regulatory_compliance", "cert_filename": "certificate_9.cer", "key_filename": "private_key_9.key", "signature_type": "regulatory_compliance", "test_data": "true", "seeder_version": "1.0"}	\N	2025-05-31 13:17:33.996664	2025-05-31 13:17:33.996665	4	3	1	chain_retail_permit_data_to_sign	SveqoJ+Mh4ERS64i2B48U9nHJ3Y8G28HJStbTtMEzeY=
\.


--
-- Data for Name: business_type_configurations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_type_configurations (id, business_type_id, municipality_id, is_disabled, has_certificate, impact_level) FROM stdin;
1	1	1	f	t	2
2	2	1	f	t	1
3	3	1	t	f	3
4	4	1	f	f	2
5	5	1	f	t	1
542	8	2	t	f	\N
543	12	2	t	f	\N
544	13	2	t	f	\N
545	14	2	t	f	\N
546	15	2	t	f	\N
547	16	2	t	f	\N
548	17	2	t	f	\N
549	18	2	t	f	\N
550	19	2	t	f	\N
551	20	2	t	f	\N
552	21	2	t	f	\N
553	22	2	t	f	\N
554	23	2	t	f	\N
555	24	2	t	f	\N
556	25	2	t	f	\N
557	26	2	t	f	\N
558	27	2	t	f	\N
559	28	2	t	f	\N
560	29	2	t	f	\N
561	30	2	t	f	\N
562	31	2	t	f	\N
563	32	2	t	f	\N
564	33	2	t	f	\N
565	34	2	t	f	\N
566	35	2	t	f	\N
567	36	2	t	f	\N
568	37	2	t	f	\N
569	38	2	t	f	\N
570	39	2	t	f	\N
571	40	2	t	f	\N
572	41	2	t	f	\N
573	42	2	t	f	\N
574	43	2	t	f	\N
575	44	2	t	f	\N
576	45	2	t	f	\N
577	46	2	t	f	\N
578	47	2	t	f	\N
579	48	2	t	f	\N
580	49	2	t	f	\N
581	50	2	t	f	\N
582	51	2	t	f	\N
583	52	2	t	f	\N
584	53	2	t	f	\N
585	54	2	t	f	\N
586	55	2	t	f	\N
587	56	2	t	f	\N
588	57	2	t	f	\N
589	58	2	t	f	\N
590	59	2	t	f	\N
591	60	2	t	f	\N
592	61	2	t	f	\N
593	62	2	t	f	\N
594	63	2	t	f	\N
595	64	2	t	f	\N
596	65	2	t	f	\N
597	66	2	t	f	\N
598	67	2	t	f	\N
599	68	2	t	f	\N
600	69	2	t	f	\N
601	70	2	t	f	\N
602	71	2	t	f	\N
603	72	2	t	f	\N
604	73	2	t	f	\N
605	74	2	t	f	\N
606	75	2	t	f	\N
607	76	2	t	f	\N
608	77	2	t	f	\N
609	78	2	t	f	\N
610	79	2	t	f	\N
611	80	2	t	f	\N
612	81	2	t	f	\N
613	82	2	t	f	\N
614	83	2	t	f	\N
615	84	2	t	f	\N
616	85	2	t	f	\N
617	86	2	t	f	\N
618	87	2	t	f	\N
619	88	2	t	f	\N
620	89	2	t	f	\N
621	90	2	t	f	\N
622	91	2	t	f	\N
623	92	2	t	f	\N
624	93	2	t	f	\N
625	94	2	t	f	\N
626	95	2	t	f	\N
627	96	2	t	f	\N
628	97	2	t	f	\N
629	98	2	t	f	\N
630	99	2	t	f	\N
631	100	2	t	f	\N
632	101	2	t	f	\N
633	102	2	t	f	\N
634	103	2	t	f	\N
635	104	2	t	f	\N
636	105	2	t	f	\N
637	106	2	t	f	\N
638	107	2	t	f	\N
639	108	2	t	f	\N
640	109	2	t	f	\N
641	110	2	t	f	\N
642	111	2	t	f	\N
643	112	2	t	f	\N
644	113	2	t	f	\N
645	114	2	t	f	\N
646	115	2	t	f	\N
647	116	2	t	f	\N
648	117	2	t	f	\N
649	118	2	t	f	\N
650	119	2	t	f	\N
651	120	2	t	f	\N
652	121	2	t	f	\N
653	122	2	t	f	\N
654	123	2	t	f	\N
655	124	2	t	f	\N
656	125	2	t	f	\N
657	126	2	t	f	\N
658	127	2	t	f	\N
659	128	2	t	f	\N
660	129	2	t	f	\N
661	130	2	t	f	\N
662	131	2	t	f	\N
663	132	2	t	f	\N
664	133	2	t	f	\N
665	134	2	t	f	\N
666	135	2	t	f	\N
667	136	2	t	f	\N
668	137	2	t	f	\N
669	138	2	t	f	\N
670	139	2	t	f	\N
671	140	2	t	f	\N
672	141	2	t	f	\N
673	142	2	t	f	\N
674	143	2	t	f	\N
675	144	2	t	f	\N
676	145	2	t	f	\N
677	146	2	t	f	\N
678	147	2	t	f	\N
679	148	2	t	f	\N
680	149	2	t	f	\N
681	150	2	t	f	\N
682	151	2	t	f	\N
683	152	2	t	f	\N
684	153	2	t	f	\N
685	154	2	t	f	\N
686	155	2	t	f	\N
687	156	2	t	f	\N
688	157	2	t	f	\N
689	158	2	t	f	\N
690	159	2	t	f	\N
691	160	2	t	f	\N
692	161	2	t	f	\N
693	162	2	t	f	\N
694	163	2	t	f	\N
695	164	2	t	f	\N
696	165	2	t	f	\N
697	166	2	t	f	\N
698	167	2	t	f	\N
699	168	2	t	f	\N
700	169	2	t	f	\N
701	170	2	t	f	\N
702	171	2	t	f	\N
703	172	2	t	f	\N
704	173	2	t	f	\N
705	174	2	t	f	\N
706	175	2	t	f	\N
707	176	2	t	f	\N
708	177	2	t	f	\N
709	178	2	t	f	\N
710	179	2	t	f	\N
711	180	2	t	f	\N
712	181	2	t	f	\N
713	182	2	t	f	\N
714	183	2	t	f	\N
715	184	2	t	f	\N
716	185	2	t	f	\N
717	186	2	t	f	\N
718	187	2	t	f	\N
719	188	2	t	f	\N
720	189	2	t	f	\N
721	190	2	t	f	\N
722	191	2	t	f	\N
723	192	2	t	f	\N
724	193	2	t	f	\N
725	194	2	t	f	\N
726	195	2	t	f	\N
727	196	2	t	f	\N
728	197	2	t	f	\N
729	198	2	t	f	\N
730	199	2	t	f	\N
731	200	2	t	f	\N
732	201	2	t	f	\N
733	202	2	t	f	\N
734	203	2	t	f	\N
735	204	2	t	f	\N
736	205	2	t	f	\N
737	206	2	t	f	\N
738	207	2	t	f	\N
739	208	2	t	f	\N
740	209	2	t	f	\N
741	210	2	t	f	\N
742	211	2	t	f	\N
743	212	2	t	f	\N
744	213	2	t	f	\N
745	214	2	t	f	\N
746	215	2	t	f	\N
747	216	2	t	f	\N
748	217	2	t	f	\N
749	218	2	t	f	\N
750	219	2	t	f	\N
751	220	2	t	f	\N
752	221	2	t	f	\N
753	222	2	t	f	\N
754	223	2	t	f	\N
755	224	2	t	f	\N
756	225	2	t	f	\N
757	226	2	t	f	\N
758	227	2	t	f	\N
759	228	2	t	f	\N
760	229	2	t	f	\N
761	230	2	t	f	\N
762	231	2	t	f	\N
763	232	2	t	f	\N
764	233	2	t	f	\N
765	234	2	t	f	\N
766	235	2	t	f	\N
767	236	2	t	f	\N
768	237	2	t	f	\N
769	238	2	t	f	\N
770	239	2	t	f	\N
771	240	2	t	f	\N
772	241	2	t	f	\N
773	242	2	t	f	\N
774	243	2	t	f	\N
775	244	2	t	f	\N
776	245	2	t	f	\N
777	246	2	t	f	\N
778	247	2	t	f	\N
779	248	2	t	f	\N
780	249	2	t	f	\N
781	250	2	t	f	\N
782	251	2	t	f	\N
783	252	2	t	f	\N
784	253	2	t	f	\N
785	254	2	t	f	\N
786	255	2	t	f	\N
787	256	2	t	f	\N
788	257	2	t	f	\N
789	258	2	t	f	\N
790	259	2	t	f	\N
791	260	2	t	f	\N
792	261	2	t	f	\N
793	262	2	t	f	\N
794	263	2	t	f	\N
795	264	2	t	f	\N
796	265	2	t	f	\N
797	266	2	t	f	\N
798	267	2	t	f	\N
799	268	2	t	f	\N
800	269	2	t	f	\N
801	270	2	t	f	\N
802	271	2	t	f	\N
803	272	2	t	f	\N
804	273	2	t	f	\N
805	274	2	t	f	\N
806	275	2	t	f	\N
807	276	2	t	f	\N
808	277	2	t	f	\N
809	278	2	t	f	\N
810	279	2	t	f	\N
811	280	2	t	f	\N
812	281	2	t	f	\N
813	282	2	t	f	\N
814	283	2	t	f	\N
815	284	2	t	f	\N
816	285	2	t	f	\N
817	286	2	t	f	\N
818	287	2	t	f	\N
819	288	2	t	f	\N
820	289	2	t	f	\N
821	290	2	t	f	\N
822	291	2	t	f	\N
823	292	2	t	f	\N
824	293	2	t	f	\N
825	294	2	t	f	\N
826	295	2	t	f	\N
827	296	2	t	f	\N
828	297	2	t	f	\N
829	298	2	t	f	\N
830	299	2	t	f	\N
831	300	2	t	f	\N
832	301	2	t	f	\N
833	302	2	t	f	\N
834	303	2	t	f	\N
835	304	2	t	f	\N
836	305	2	t	f	\N
837	306	2	t	f	\N
838	307	2	t	f	\N
839	308	2	t	f	\N
840	309	2	t	f	\N
841	310	2	t	f	\N
842	311	2	t	f	\N
843	312	2	t	f	\N
844	313	2	t	f	\N
845	314	2	t	f	\N
846	315	2	t	f	\N
847	316	2	t	f	\N
848	317	2	t	f	\N
849	318	2	t	f	\N
850	319	2	t	f	\N
851	320	2	t	f	\N
852	321	2	t	f	\N
853	322	2	t	f	\N
854	323	2	t	f	\N
855	324	2	t	f	\N
856	325	2	t	f	\N
857	326	2	t	f	\N
858	327	2	t	f	\N
859	328	2	t	f	\N
860	329	2	t	f	\N
861	330	2	t	f	\N
862	331	2	t	f	\N
863	332	2	t	f	\N
864	333	2	t	f	\N
865	334	2	t	f	\N
866	335	2	t	f	\N
867	336	2	t	f	\N
868	337	2	t	f	\N
869	338	2	t	f	\N
870	339	2	t	f	\N
871	340	2	t	f	\N
872	341	2	t	f	\N
873	342	2	t	f	\N
874	343	2	t	f	\N
875	344	2	t	f	\N
876	345	2	t	f	\N
877	346	2	t	f	\N
878	347	2	t	f	\N
879	348	2	t	f	\N
880	349	2	t	f	\N
881	350	2	t	f	\N
882	351	2	t	f	\N
883	352	2	t	f	\N
884	353	2	t	f	\N
885	354	2	t	f	\N
886	355	2	t	f	\N
887	356	2	t	f	\N
888	357	2	t	f	\N
889	358	2	t	f	\N
890	359	2	t	f	\N
891	360	2	t	f	\N
892	361	2	t	f	\N
893	362	2	t	f	\N
894	363	2	t	f	\N
895	364	2	t	f	\N
896	365	2	t	f	\N
897	366	2	t	f	\N
898	367	2	t	f	\N
899	368	2	t	f	\N
900	369	2	t	f	\N
901	370	2	t	f	\N
902	371	2	t	f	\N
903	372	2	t	f	\N
904	373	2	t	f	\N
905	374	2	t	f	\N
906	375	2	t	f	\N
907	376	2	t	f	\N
908	377	2	t	f	\N
909	378	2	t	f	\N
910	379	2	t	f	\N
911	380	2	t	f	\N
912	381	2	t	f	\N
913	382	2	t	f	\N
914	383	2	t	f	\N
915	384	2	t	f	\N
916	385	2	t	f	\N
917	386	2	t	f	\N
918	387	2	t	f	\N
919	388	2	t	f	\N
920	389	2	t	f	\N
921	390	2	t	f	\N
922	391	2	t	f	\N
923	392	2	t	f	\N
924	393	2	t	f	\N
925	394	2	t	f	\N
926	395	2	t	f	\N
927	396	2	t	f	\N
928	397	2	t	f	\N
929	398	2	t	f	\N
930	399	2	t	f	\N
931	400	2	t	f	\N
932	401	2	t	f	\N
933	402	2	t	f	\N
934	403	2	t	f	\N
935	404	2	t	f	\N
936	405	2	t	f	\N
937	406	2	t	f	\N
938	407	2	t	f	\N
939	408	2	t	f	\N
940	409	2	t	f	\N
941	410	2	t	f	\N
942	411	2	t	f	\N
943	412	2	t	f	\N
944	413	2	t	f	\N
945	414	2	t	f	\N
946	415	2	t	f	\N
947	416	2	t	f	\N
948	417	2	t	f	\N
949	418	2	t	f	\N
950	419	2	t	f	\N
951	420	2	t	f	\N
952	421	2	t	f	\N
953	422	2	t	f	\N
954	423	2	t	f	\N
955	424	2	t	f	\N
956	425	2	t	f	\N
957	426	2	t	f	\N
958	427	2	t	f	\N
959	428	2	t	f	\N
960	429	2	t	f	\N
961	430	2	t	f	\N
962	431	2	t	f	\N
963	432	2	t	f	\N
964	433	2	t	f	\N
965	434	2	t	f	\N
966	435	2	t	f	\N
967	436	2	t	f	\N
968	437	2	t	f	\N
969	438	2	t	f	\N
970	439	2	t	f	\N
971	440	2	t	f	\N
972	441	2	t	f	\N
973	442	2	t	f	\N
974	443	2	t	f	\N
975	444	2	t	f	\N
976	445	2	t	f	\N
977	446	2	t	f	\N
978	447	2	t	f	\N
979	448	2	t	f	\N
980	449	2	t	f	\N
981	450	2	t	f	\N
982	451	2	t	f	\N
983	452	2	t	f	\N
984	453	2	t	f	\N
985	454	2	t	f	\N
986	455	2	t	f	\N
987	456	2	t	f	\N
988	457	2	t	f	\N
989	458	2	t	f	\N
990	459	2	t	f	\N
991	460	2	t	f	\N
992	461	2	t	f	\N
993	462	2	t	f	\N
994	463	2	t	f	\N
995	464	2	t	f	\N
996	465	2	t	f	\N
997	466	2	t	f	\N
998	467	2	t	f	\N
999	468	2	t	f	\N
1000	469	2	t	f	\N
1001	470	2	t	f	\N
1002	471	2	t	f	\N
1003	472	2	t	f	\N
1004	473	2	t	f	\N
1005	474	2	t	f	\N
1006	475	2	t	f	\N
1007	476	2	t	f	\N
1008	477	2	t	f	\N
1009	478	2	t	f	\N
1010	479	2	t	f	\N
1011	480	2	t	f	\N
1012	481	2	t	f	\N
1013	482	2	t	f	\N
1014	483	2	t	f	\N
1015	484	2	t	f	\N
1016	485	2	t	f	\N
1017	486	2	t	f	\N
1018	487	2	t	f	\N
1019	488	2	t	f	\N
1020	489	2	t	f	\N
1021	490	2	t	f	\N
1022	491	2	t	f	\N
1023	492	2	t	f	\N
1024	493	2	t	f	\N
1025	494	2	t	f	\N
1026	495	2	t	f	\N
1027	496	2	t	f	\N
1028	497	2	t	f	\N
1029	498	2	t	f	\N
1030	499	2	t	f	\N
1031	500	2	t	f	\N
1032	501	2	t	f	\N
1033	502	2	t	f	\N
1034	503	2	t	f	\N
1035	504	2	t	f	\N
1036	505	2	t	f	\N
1037	506	2	t	f	\N
1038	507	2	t	f	\N
1039	508	2	t	f	\N
1040	509	2	t	f	\N
1041	510	2	t	f	\N
1042	511	2	t	f	\N
1043	512	2	t	f	\N
1044	513	2	t	f	\N
1045	514	2	t	f	\N
1046	515	2	t	f	\N
1047	516	2	t	f	\N
1048	517	2	t	f	\N
1049	518	2	t	f	\N
1050	519	2	t	f	\N
1051	520	2	t	f	\N
1052	521	2	t	f	\N
1053	522	2	t	f	\N
1054	523	2	t	f	\N
1055	524	2	t	f	\N
1056	525	2	t	f	\N
1057	526	2	t	f	\N
1058	527	2	t	f	\N
1059	528	2	t	f	\N
1060	529	2	t	f	\N
1061	530	2	t	f	\N
1062	531	2	t	f	\N
1063	532	2	t	f	\N
1064	533	2	t	f	\N
1065	534	2	t	f	\N
1066	535	2	t	f	\N
1067	536	2	t	f	\N
1068	537	2	t	f	\N
1069	538	2	t	f	\N
1070	539	2	t	f	\N
1071	540	2	t	f	\N
1072	541	2	t	f	\N
1073	542	2	t	f	\N
1074	543	2	t	f	\N
1075	544	2	t	f	\N
1076	545	2	t	f	\N
1077	546	2	t	f	\N
1078	547	2	t	f	\N
1079	548	2	t	f	\N
1080	549	2	t	f	\N
1081	550	2	t	f	\N
1082	551	2	t	f	\N
1083	552	2	t	f	\N
1084	553	2	t	f	\N
1085	554	2	t	f	\N
1086	555	2	t	f	\N
1087	556	2	t	f	\N
1088	558	2	t	f	\N
1089	559	2	t	f	\N
1090	560	2	t	f	\N
1091	561	2	t	f	\N
1092	562	2	t	f	\N
1093	563	2	t	f	\N
1094	564	2	t	f	\N
1095	565	2	t	f	\N
1096	566	2	t	f	\N
1097	567	2	t	f	\N
1098	568	2	t	f	\N
1099	569	2	t	f	\N
1100	570	2	t	f	\N
1101	571	2	t	f	\N
1102	572	2	t	f	\N
1103	573	2	t	f	\N
1104	574	2	t	f	\N
1105	575	2	t	f	\N
1106	576	2	t	f	\N
1107	577	2	t	f	\N
1108	578	2	t	f	\N
1109	579	2	t	f	\N
1110	580	2	t	f	\N
1111	581	2	t	f	\N
1112	582	2	t	f	\N
1113	583	2	t	f	\N
1114	584	2	t	f	\N
1115	585	2	t	f	\N
1116	586	2	t	f	\N
1117	587	2	t	f	\N
1118	588	2	t	f	\N
1119	589	2	t	f	\N
1120	590	2	t	f	\N
1121	591	2	t	f	\N
1122	592	2	t	f	\N
1123	593	2	t	f	\N
1124	594	2	t	f	\N
1125	595	2	t	f	\N
1126	596	2	t	f	\N
1127	597	2	t	f	\N
1128	598	2	t	f	\N
1129	599	2	t	f	\N
1130	600	2	t	f	\N
1131	601	2	t	f	\N
1132	602	2	t	f	\N
1133	603	2	t	f	\N
1134	604	2	t	f	\N
1135	605	2	t	f	\N
1136	606	2	t	f	\N
1137	607	2	t	f	\N
1138	608	2	t	f	\N
1139	609	2	t	f	\N
1140	610	2	t	f	\N
1141	611	2	t	f	\N
1142	612	2	t	f	\N
1143	613	2	t	f	\N
1144	614	2	t	f	\N
1145	615	2	t	f	\N
1146	616	2	t	f	\N
1147	617	2	t	f	\N
1148	618	2	t	f	\N
1149	619	2	t	f	\N
1150	620	2	t	f	\N
1151	621	2	t	f	\N
1152	622	2	t	f	\N
1153	623	2	t	f	\N
1154	624	2	t	f	\N
1155	625	2	t	f	\N
1156	626	2	t	f	\N
1157	627	2	t	f	\N
1158	628	2	t	f	\N
1159	629	2	t	f	\N
1160	630	2	t	f	\N
1161	631	2	t	f	\N
1162	632	2	t	f	\N
1163	633	2	t	f	\N
1164	634	2	t	f	\N
1165	635	2	t	f	\N
1166	636	2	t	f	\N
1167	637	2	t	f	\N
1168	638	2	t	f	\N
1169	639	2	t	f	\N
1170	640	2	t	f	\N
1171	641	2	t	f	\N
1172	642	2	t	f	\N
1173	643	2	t	f	\N
1174	644	2	t	f	\N
1175	645	2	t	f	\N
1176	646	2	t	f	\N
1177	647	2	t	f	\N
1178	648	2	t	f	\N
1179	649	2	t	f	\N
1180	650	2	t	f	\N
1181	651	2	t	f	\N
1182	652	2	t	f	\N
1183	653	2	t	f	\N
1184	654	2	t	f	\N
1185	655	2	t	f	\N
1186	656	2	t	f	\N
1187	657	2	t	f	\N
1188	658	2	t	f	\N
1189	659	2	t	f	\N
1190	660	2	t	f	\N
1191	661	2	t	f	\N
1192	662	2	t	f	\N
1193	663	2	t	f	\N
1194	664	2	t	f	\N
1195	665	2	t	f	\N
1196	666	2	t	f	\N
1197	667	2	t	f	\N
1198	668	2	t	f	\N
1199	669	2	t	f	\N
1200	670	2	t	f	\N
1201	671	2	t	f	\N
1202	672	2	t	f	\N
1203	673	2	t	f	\N
1204	674	2	t	f	\N
1205	675	2	t	f	\N
1206	676	2	t	f	\N
1207	677	2	t	f	\N
1208	678	2	t	f	\N
1209	679	2	t	f	\N
1210	680	2	t	f	\N
1211	681	2	t	f	\N
1212	682	2	t	f	\N
1213	683	2	t	f	\N
1214	684	2	t	f	\N
1215	685	2	t	f	\N
1216	686	2	t	f	\N
1217	687	2	t	f	\N
1218	688	2	t	f	\N
1219	689	2	t	f	\N
1220	690	2	t	f	\N
1221	691	2	t	f	\N
1222	692	2	t	f	\N
1223	693	2	t	f	\N
1224	694	2	t	f	\N
1225	695	2	t	f	\N
1226	696	2	t	f	\N
1227	697	2	t	f	\N
1228	698	2	t	f	\N
1229	699	2	t	f	\N
1230	700	2	t	f	\N
1231	701	2	t	f	\N
1232	702	2	t	f	\N
1233	703	2	t	f	\N
1234	704	2	t	f	\N
1235	705	2	t	f	\N
1236	706	2	t	f	\N
1237	707	2	t	f	\N
1238	708	2	t	f	\N
1239	709	2	t	f	\N
1240	710	2	t	f	\N
1241	711	2	t	f	\N
1242	712	2	t	f	\N
1243	713	2	t	f	\N
1244	714	2	t	f	\N
1245	715	2	t	f	\N
1246	716	2	t	f	\N
1247	717	2	t	f	\N
1248	718	2	t	f	\N
1249	719	2	t	f	\N
1250	720	2	t	f	\N
1251	721	2	t	f	\N
1252	722	2	t	f	\N
1253	723	2	t	f	\N
1254	724	2	t	f	\N
1255	725	2	t	f	\N
1256	726	2	t	f	\N
1257	727	2	t	f	\N
1258	728	2	t	f	\N
1259	729	2	t	f	\N
1260	730	2	t	f	\N
1261	731	2	t	f	\N
1262	732	2	t	f	\N
1263	733	2	t	f	\N
1264	734	2	t	f	\N
1265	735	2	t	f	\N
1266	736	2	t	f	\N
1267	737	2	t	f	\N
1268	738	2	t	f	\N
1269	739	2	t	f	\N
1270	740	2	t	f	\N
1271	741	2	t	f	\N
1272	742	2	t	f	\N
1273	743	2	t	f	\N
1274	744	2	t	f	\N
1275	745	2	t	f	\N
1276	746	2	t	f	\N
1277	747	2	t	f	\N
1278	748	2	t	f	\N
1279	749	2	t	f	\N
1280	750	2	t	f	\N
1281	751	2	t	f	\N
1282	752	2	t	f	\N
1283	753	2	t	f	\N
1284	754	2	t	f	\N
1285	755	2	t	f	\N
1286	756	2	t	f	\N
1287	757	2	t	f	\N
1288	758	2	t	f	\N
1289	759	2	t	f	\N
1290	760	2	t	f	\N
1291	761	2	t	f	\N
1292	762	2	t	f	\N
1293	763	2	t	f	\N
1294	764	2	t	f	\N
1295	765	2	t	f	\N
1296	766	2	t	f	\N
1297	767	2	t	f	\N
1298	768	2	t	f	\N
1299	769	2	t	f	\N
1300	770	2	t	f	\N
1301	771	2	t	f	\N
1302	772	2	t	f	\N
1303	773	2	t	f	\N
1304	774	2	t	f	\N
1305	775	2	t	f	\N
1306	776	2	t	f	\N
1307	777	2	t	f	\N
1308	778	2	t	f	\N
1309	779	2	t	f	\N
1310	780	2	t	f	\N
1311	781	2	t	f	\N
1312	782	2	t	f	\N
1313	783	2	t	f	\N
1314	784	2	t	f	\N
1315	785	2	t	f	\N
1316	786	2	t	f	\N
1317	787	2	t	f	\N
1318	788	2	t	f	\N
1319	789	2	t	f	\N
1320	790	2	t	f	\N
1321	791	2	t	f	\N
1322	792	2	t	f	\N
1323	793	2	t	f	\N
1324	794	2	t	f	\N
1325	795	2	t	f	\N
1326	796	2	t	f	\N
1327	797	2	t	f	\N
1328	798	2	t	f	\N
1329	799	2	t	f	\N
1330	800	2	t	f	\N
1331	801	2	t	f	\N
1332	802	2	t	f	\N
1333	803	2	t	f	\N
1334	804	2	t	f	\N
1335	805	2	t	f	\N
1336	806	2	t	f	\N
1337	807	2	t	f	\N
1338	808	2	t	f	\N
1339	809	2	t	f	\N
1340	810	2	t	f	\N
1341	811	2	t	f	\N
1342	812	2	t	f	\N
1343	813	2	t	f	\N
1344	814	2	t	f	\N
1345	815	2	t	f	\N
1346	816	2	t	f	\N
1347	817	2	t	f	\N
1348	818	2	t	f	\N
1349	819	2	t	f	\N
1350	820	2	t	f	\N
1351	821	2	t	f	\N
1352	822	2	t	f	\N
1353	823	2	t	f	\N
1354	824	2	t	f	\N
1355	825	2	t	f	\N
1356	826	2	t	f	\N
1357	827	2	t	f	\N
1358	828	2	t	f	\N
1359	829	2	t	f	\N
1360	830	2	t	f	\N
1361	831	2	t	f	\N
1362	832	2	t	f	\N
1363	833	2	t	f	\N
1364	834	2	t	f	\N
1365	835	2	t	f	\N
1366	836	2	t	f	\N
1367	837	2	t	f	\N
1368	838	2	t	f	\N
1369	839	2	t	f	\N
1370	840	2	t	f	\N
1371	841	2	t	f	\N
1372	842	2	t	f	\N
1373	843	2	t	f	\N
1374	844	2	t	f	\N
1375	845	2	t	f	\N
1376	846	2	t	f	\N
1377	847	2	t	f	\N
1378	848	2	t	f	\N
1379	849	2	t	f	\N
1380	850	2	t	f	\N
1381	851	2	t	f	\N
1382	852	2	t	f	\N
1383	853	2	t	f	\N
1384	854	2	t	f	\N
1385	855	2	t	f	\N
1386	856	2	t	f	\N
1387	857	2	t	f	\N
1388	858	2	t	f	\N
1389	859	2	t	f	\N
1390	860	2	t	f	\N
1391	861	2	t	f	\N
1392	862	2	t	f	\N
1393	863	2	t	f	\N
1394	864	2	t	f	\N
1395	865	2	t	f	\N
1396	866	2	t	f	\N
1397	867	2	t	f	\N
1398	868	2	t	f	\N
1399	869	2	t	f	\N
1400	870	2	t	f	\N
1401	871	2	t	f	\N
1402	872	2	t	f	\N
1403	873	2	t	f	\N
1404	874	2	t	f	\N
1405	875	2	t	f	\N
1406	876	2	t	f	\N
1407	877	2	t	f	\N
1408	878	2	t	f	\N
1409	879	2	t	f	\N
1410	880	2	t	f	\N
1411	881	2	t	f	\N
1412	882	2	t	f	\N
1413	883	2	t	f	\N
1414	884	2	t	f	\N
1415	885	2	t	f	\N
1416	886	2	t	f	\N
1417	887	2	t	f	\N
1418	888	2	t	f	\N
1419	889	2	t	f	\N
1420	890	2	t	f	\N
1421	891	2	t	f	\N
1422	892	2	t	f	\N
1423	893	2	t	f	\N
1424	894	2	t	f	\N
1425	895	2	t	f	\N
1426	896	2	t	f	\N
1427	897	2	t	f	\N
1428	898	2	t	f	\N
1429	899	2	t	f	\N
1430	900	2	t	f	\N
1431	901	2	t	f	\N
1432	902	2	t	f	\N
1433	903	2	t	f	\N
1434	904	2	t	f	\N
1435	905	2	t	f	\N
1436	906	2	t	f	\N
1437	907	2	t	f	\N
1438	908	2	t	f	\N
1439	909	2	t	f	\N
1440	910	2	t	f	\N
1441	911	2	t	f	\N
1442	912	2	t	f	\N
1443	913	2	t	f	\N
1444	914	2	t	f	\N
1445	915	2	t	f	\N
1446	916	2	t	f	\N
1447	917	2	t	f	\N
1448	918	2	t	f	\N
1449	919	2	t	f	\N
1450	920	2	t	f	\N
1451	921	2	t	f	\N
1452	922	2	t	f	\N
1453	923	2	t	f	\N
1454	924	2	t	f	\N
1455	925	2	t	f	\N
1456	926	2	t	f	\N
1457	927	2	t	f	\N
1458	928	2	t	f	\N
1459	929	2	t	f	\N
1460	930	2	t	f	\N
1461	931	2	t	f	\N
1462	932	2	t	f	\N
1463	933	2	t	f	\N
1464	934	2	t	f	\N
1465	935	2	t	f	\N
1466	936	2	t	f	\N
1467	937	2	t	f	\N
1468	938	2	t	f	\N
1469	939	2	t	f	\N
1470	940	2	t	f	\N
1471	941	2	t	f	\N
1472	942	2	t	f	\N
1473	943	2	t	f	\N
1474	944	2	t	f	\N
1475	945	2	t	f	\N
1476	946	2	t	f	\N
1477	947	2	t	f	\N
1478	948	2	t	f	\N
1479	949	2	t	f	\N
1480	950	2	t	f	\N
1481	951	2	t	f	\N
1482	952	2	t	f	\N
1483	953	2	t	f	\N
1484	954	2	t	f	\N
1485	955	2	t	f	\N
1486	956	2	t	f	\N
1487	957	2	t	f	\N
1488	958	2	t	f	\N
1489	959	2	t	f	\N
1490	960	2	t	f	\N
1491	961	2	t	f	\N
1492	962	2	t	f	\N
1493	963	2	t	f	\N
1494	964	2	t	f	\N
1495	965	2	t	f	\N
1496	966	2	t	f	\N
1497	967	2	t	f	\N
1498	968	2	t	f	\N
1499	969	2	t	f	\N
1500	970	2	t	f	\N
1501	971	2	t	f	\N
1502	972	2	t	f	\N
1503	973	2	t	f	\N
1504	974	2	t	f	\N
1505	975	2	t	f	\N
1506	976	2	t	f	\N
1507	977	2	t	f	\N
1508	978	2	t	f	\N
1509	979	2	t	f	\N
1510	980	2	t	f	\N
1511	981	2	t	f	\N
1512	982	2	t	f	\N
1513	983	2	t	f	\N
1514	984	2	t	f	\N
1515	985	2	t	f	\N
1516	986	2	t	f	\N
1517	987	2	t	f	\N
1518	988	2	t	f	\N
1519	989	2	t	f	\N
1520	990	2	t	f	\N
1521	991	2	t	f	\N
1522	992	2	t	f	\N
1523	993	2	t	f	\N
1524	994	2	t	f	\N
1525	995	2	t	f	\N
1526	996	2	t	f	\N
1527	997	2	t	f	\N
1528	998	2	t	f	\N
1529	999	2	t	f	\N
1530	1000	2	t	f	\N
1531	1001	2	t	f	\N
1532	1002	2	t	f	\N
1533	1003	2	t	f	\N
1534	1004	2	t	f	\N
1535	1005	2	t	f	\N
1536	1006	2	t	f	\N
1537	1007	2	t	f	\N
1538	1008	2	t	f	\N
1539	1009	2	t	f	\N
1540	1010	2	t	f	\N
1541	1011	2	t	f	\N
1542	1012	2	t	f	\N
1543	1013	2	t	f	\N
1544	1014	2	t	f	\N
1545	1015	2	t	f	\N
1546	1016	2	t	f	\N
1547	1017	2	t	f	\N
1548	1018	2	t	f	\N
1549	1019	2	t	f	\N
1550	1020	2	t	f	\N
1551	1021	2	t	f	\N
1552	1022	2	t	f	\N
1553	1023	2	t	f	\N
1554	1024	2	t	f	\N
1555	1025	2	t	f	\N
1556	1026	2	t	f	\N
1557	1027	2	t	f	\N
1558	1028	2	t	f	\N
1559	1029	2	t	f	\N
1560	1030	2	t	f	\N
1561	1031	2	t	f	\N
1562	1032	2	t	f	\N
1563	1033	2	t	f	\N
1564	1034	2	t	f	\N
1565	1035	2	t	f	\N
1566	1036	2	t	f	\N
1567	1037	2	t	f	\N
1568	1038	2	t	f	\N
1569	1039	2	t	f	\N
1570	1040	2	t	f	\N
1571	1041	2	t	f	\N
1572	1042	2	t	f	\N
1573	1043	2	t	f	\N
1574	1044	2	t	f	\N
1575	1045	2	t	f	\N
1576	1046	2	t	f	\N
1577	1047	2	t	f	\N
1578	1048	2	t	f	\N
1579	1049	2	t	f	\N
1580	1050	2	t	f	\N
1581	1051	2	t	f	\N
1582	1052	2	t	f	\N
1583	1053	2	t	f	\N
1584	1054	2	t	f	\N
1585	1055	2	t	f	\N
1586	1056	2	t	f	\N
1587	1057	2	t	f	\N
1588	1058	2	t	f	\N
1589	1059	2	t	f	\N
1590	1060	2	t	f	\N
1591	1061	2	t	f	\N
1592	1062	2	t	f	\N
1593	1063	2	t	f	\N
1594	1064	2	t	f	\N
1595	1065	2	t	f	\N
1596	1066	2	t	f	\N
1597	1067	2	t	f	\N
1598	1068	2	t	f	\N
1599	1069	2	t	f	\N
1600	1070	2	t	f	\N
1601	1071	2	t	f	\N
1602	1072	2	t	f	\N
1603	1073	2	t	f	\N
1604	1074	2	t	f	\N
1605	1075	2	t	f	\N
1606	1076	2	t	f	\N
1607	1077	2	t	f	\N
1608	1078	2	t	f	\N
1609	1079	2	t	f	\N
1610	1080	2	t	f	\N
1611	1081	2	t	f	\N
1612	1082	2	t	f	\N
1613	1083	2	t	f	\N
1614	1084	2	t	f	\N
1615	1085	2	t	f	\N
1616	1086	2	t	f	\N
1617	1087	2	t	f	\N
1618	1088	2	t	f	\N
1619	1089	2	t	f	\N
1620	1090	2	t	f	\N
1621	1091	2	t	f	\N
1622	1092	2	t	f	\N
1623	7	2	f	f	1
1624	9	2	f	f	1
1625	10	2	f	f	1
1626	11	2	f	f	1
1627	557	2	f	f	0
\.


--
-- Data for Name: business_types; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.business_types (id, name, description, is_active, code, related_words) FROM stdin;
1	Retail Store	General retail business	t	\N	\N
2	Pharmacy	Establishment that sells medicine and health products	t	\N	\N
3	Bar or Nightclub	Entertainment venue	t	\N	\N
4	Auto Repair Shop	Mechanical service and repair	t	\N	\N
5	Bakery	Production and sale of baked goods	t	\N	\N
6	Test Business Type	A test business type for verification	t	\N	\N
7	Cultivo de soya	frijoles de soya (grano) orgánicos, cultivo, frijoles de soya (grano), cultivo, soya (grano), cultivo, soya bragg (grano), cultivo, soya bragg orgánica (grano), cultivo, soya cajeme (grano), cultivo, soya cajeme orgánica (grano), cultivo, soya davis (grano), cultivo, soya davis orgánica (grano), cultivo, soya hood (grano), cultivo, soya hood orgánica (grano), cultivo, soya mayo (grano), cultivo, soya mayo orgánica (grano), cultivo, soya orgánica (grano), cultivo, soya Santa Rosa (grano), cultivo	t	\N	\N
8	Cultivo de cártamo	cártamo (semilla), cultivo, cártamo kino (semilla), cultivo, cártamo kino orgánico (semilla), cultivo, cártamo macarena (semilla), cultivo, cártamo macarena orgánico (semilla), cultivo, cártamo mante (semilla), cultivo, cártamo mante orgánico (semilla), cultivo, cártamo orgánico (semilla), cultivo, cártamo saffola (semilla), cultivo, cártamo saffola orgánico (semilla), cultivo	t	\N	\N
9	Cultivo de girasol	flores de sol (semilla), cultivo, flores de sol orgánicas (semilla), cultivo, gigantones (semilla), cultivo, gigantones orgánicos (semilla), cultivo, girasoles (semilla), cultivo, girasoles orgánicos (semilla), cultivo, maíz de tejas (semilla), cultivo, maíz de tejas orgánico (semilla), cultivo	t	\N	\N
10	Cultivo anual de otras semillas oleaginosas	ajonjolí anual (semilla), cultivo, ajonjolí orgánico anual (semilla), cultivo, canola anual (semilla), cultivo, canola orgánica anual (semilla), cultivo, chilacayotes anuales (semilla), cultivo, chilacayotes orgánicos anuales (semilla), cultivo, colzas anuales (semilla), cultivo, colzas orgánicas anuales (semilla), cultivo, cultivo de diferentes semillas oleaginosas cuando sea imposible determinar cuál es el principal, deghas anuales (semilla), cultivo, deghas orgánicas anuales (semilla), cultiv	t	\N	\N
11	Cultivo de frijol grano	acalete (grano), cultivo, acalete orgánico (grano), cultivo, alubia (grano), cultivo, alubia orgánica (grano), cultivo, ayocote (grano), cultivo, ayocote orgánico (grano), cultivo, choreque (grano), cultivo, choreque orgánico (grano), cultivo, colon cahui (grano), cultivo, colon cahui orgánico (grano), cultivo, conchite (grano), cultivo, conchite orgánico (grano), cultivo, duh-chi (grano), cultivo, duh-chi orgánico (grano), cultivo, escomite (grano), cultivo, escomite orgánico (grano), cultivo, 	t	\N	\N
12	Cultivo de garbanzo grano	garbanzos (grano), cultivo, garbanzos orgánicos (grano), cultivo, garbanzos puerqueros (grano), cultivo	t	\N	\N
13	Cultivo de otras leguminosas	algarrobas (grano), cultivo, algarrobas orgánicas (grano), cultivo, amargones (grano), cultivo, amargones orgánicos (grano), cultivo, arvejas (grano), cultivo, arvejas orgánicas (grano), cultivo, arvejones (grano), cultivo, arvejones orgánicos (grano), cultivo, canavalias (grano), cultivo, canavalias orgánicas (grano), cultivo, carretillas (grano), cultivo, carretillas orgánicas (grano), cultivo, chícharos (forraje), cultivo, chícharos (grano), cultivo, chícharos orgánicos (grano), cultivo, chor	t	\N	\N
14	Cultivo de trigo	trigo (grano), cultivo, trigo aconchi (grano), cultivo, trigo aconchi orgánico (grano), cultivo, trigo altar (grano), cultivo, trigo altar orgánico (grano), cultivo, trigo angostura (grano), cultivo, trigo angostura orgánico (grano), cultivo, trigo bacanora (grano), cultivo, trigo bacanora orgánico (grano), cultivo, trigo bary (grano), cultivo, trigo bary orgánico (grano), cultivo, trigo carrizo (grano), cultivo, trigo carrizo orgánico (grano), cultivo, trigo ceric (grano), cultivo, trigo ceric 	t	\N	\N
15	Cultivo de maíz grano	maíz (grano), cultivo, maíz amarillo (grano), cultivo, maíz asgrow (grano), cultivo, maíz asgrow orgánico (grano), cultivo, maíz blanco (grano), cultivo, maíz bolita-sequía (grano), cultivo, maíz bolita-sequía orgánico (grano), cultivo, maíz cacahuazintle (grano), cultivo, maíz cacahuazintle orgánico (grano), cultivo, maíz caloro (grano), cultivo, maíz caloro orgánico (grano), cultivo, maíz cargill (grano), cultivo, maíz cargill orgánico (grano), cultivo, maíz ceres (grano), cultivo, maíz ceres 	t	\N	\N
16	Cultivo de maíz forrajero	caña maíz (forraje), cultivo, caña maíz inmadura (forraje), cultivo, caña maíz inmadura orgánica (forraje), cultivo, caña maíz orgánica (forraje), cultivo, maíz (forraje), cultivo, maíz achicalado (forraje), cultivo, maíz con la finalidad de cosechar la planta completa para aprovechamiento del ganado, cultivo, miranda (forraje), cultivo, paja de maíz (forraje), cultivo	t	\N	\N
17	Cultivo de arroz	arroz (grano), cultivo, arroz cica (grano), cultivo, arroz cica orgánico (grano), cultivo, arroz Morelos (grano), cultivo, arroz orgánico (grano), cultivo, arroz palay (grano), cultivo, arroz palay orgánico (grano), cultivo	t	\N	\N
48	Cultivo de chile en invernaderos y otras estructuras agrícolas protegidas	chiles (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, chiles orgánicos (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, chiles orgánicos, cultivo en invernaderos y otras estructuras agrícolas protegidas, chiles, cultivo en invernaderos y otras estructuras agrícolas protegidas	t	\N	\N
18	Cultivo de sorgo grano	espiga sorgo (grano), cultivo, espiga sorgo orgánica (grano), cultivo, malame (grano), cultivo, malame orgánico (grano), cultivo, milo (grano), cultivo, milo orgánico (grano), cultivo, milomaíz (grano), cultivo, milomaíz orgánico (grano), cultivo, sorgo (grano), cultivo, sorgo amargo (grano), cultivo, sorgo amargo orgánico (grano), cultivo, sorgo asgrow (grano), cultivo, sorgo asgrow orgánico (grano), cultivo, sorgo cargill (grano), cultivo, sorgo cargill orgánico (grano), cultivo, sorgo dekalb 	t	\N	\N
19	Cultivo de avena grano	avena (grano), cultivo, avena babícora (grano), cultivo, avena babícora orgánica (grano), cultivo, avena bachiniva (grano), cultivo, avena bachiniva orgánica (grano), cultivo, avena bacum (grano), cultivo, avena bacum orgánica (grano), cultivo, avena cevamex (grano), cultivo, avena cevamex orgánica (grano), cultivo, avena ciénega (grano), cultivo, avena ciénega orgánica (grano), cultivo, avena criolla (grano), cultivo, avena criolla orgánica (grano), cultivo, avena cusihuiriachi (grano), cultivo	t	\N	\N
20	Cultivo de cebada grano	cebada (grano), cultivo, cebada centinela (grano), cultivo, cebada centinela orgánica (grano), cultivo, cebada cerro prieto (grano), cultivo, cebada cerro prieto orgánica (grano), cultivo, cebada cervecera (grano), cultivo, cebada cervecera orgánica (grano), cultivo, cebada esmeralda (grano), cultivo, cebada esmeralda orgánica (grano), cultivo, cebada esperanza (grano), cultivo, cebada esperanza orgánica (grano), cultivo, cebada maltera (grano), cultivo, cebada maltera orgánica (grano), cultivo,	t	\N	\N
21	Cultivo de sorgo forrajero	caña sorguera (forraje), cultivo, escoba (forraje), cultivo, espiga escobera (forraje), cultivo, maicena (forraje), cultivo, malame (forraje), cultivo, paja de sorgo (forraje), cultivo, pasto sudán (forraje), cultivo, pata de sorgo (forraje), cultivo, sorgo (forraje), cultivo, sorgo con la finalidad de cosechar la planta completa para aprovechamiento del ganado, cultivo, sorgo escobero, cultivo, sorgo grazer (forraje), cultivo, sorgo kikapu (forraje), cultivo, vara de escoba (forraje), cultivo, 	t	\N	\N
22	Cultivo de avena forrajera	avena (forraje), cultivo, avena cevamex (forraje), cultivo, avena con la finalidad de cosechar la planta completa para aprovechamiento del ganado, cultivo, avena karma (forraje), cultivo, avena papigochi (forraje), cultivo, avena sala (forraje), cultivo, avena silvestre (forraje), cultivo	t	\N	\N
23	Cultivo de otros cereales	alcacer (forraje), cultivo, alpiste (fruto), cultivo, alpiste (grano), cultivo, alpiste en verde (forraje), cultivo, arroz silvestre (grano), cultivo, centeno (forraje), cultivo, centeno (grano), cultivo, cereales con la finalidad de cosechar la planta completa para aprovechamiento del ganado (excepto sorgo, avena), cultivo, cultivo de diferentes cereales cuando sea imposible determinar cuál es el principal, mijo (grano), cultivo, paja de alpiste (forraje), cultivo, paja de centeno (forraje), cu	t	\N	\N
24	Cultivo de jitomate o tomate rojo	jitomates bola mejorados orgánicos, cultivo a cielo abierto, jitomates bola mejorados, cultivo a cielo abierto, jitomates cherry orgánicos, cultivo a cielo abierto, jitomates cherry, cultivo a cielo abierto, jitomates chitalino orgánicos, cultivo a cielo abierto, jitomates chitalino, cultivo a cielo abierto, jitomates de monte orgánicos, cultivo a cielo abierto, jitomates de monte, cultivo a cielo abierto, jitomates de vara orgánicos, cultivo a cielo abierto, jitomates de vara, cultivo a cielo a	t	\N	\N
25	Cultivo de chile	chak'ik orgánicos, cultivo a cielo abierto, chak'ik, cultivo a cielo abierto, chiles acorchados orgánicos, cultivo a cielo abierto, chiles acorchados, cultivo a cielo abierto, chiles altamira orgánicos, cultivo a cielo abierto, chiles altamira, cultivo a cielo abierto, chiles anchos orgánicos, cultivo a cielo abierto, chiles anchos, cultivo a cielo abierto, chiles bell orgánicos, cultivo a cielo abierto, chiles bell, cultivo a cielo abierto, chiles bola orgánicos, cultivo a cielo abierto, chiles	t	\N	\N
26	Cultivo de cebolla	cebollas bola orgánicas, cultivo a cielo abierto, cebollas bola, cultivo a cielo abierto, cebollas cambray orgánicas, cultivo a cielo abierto, cebollas cambray, cultivo a cielo abierto, cebollas cimarronas orgánicas, cultivo a cielo abierto, cebollas cimarronas, cultivo a cielo abierto, cebollas criollas orgánicas, cultivo a cielo abierto, cebollas criollas, cultivo a cielo abierto, cebollas de ixil orgánicas, cultivo a cielo abierto, cebollas de ixil, cultivo a cielo abierto, cebollas de monte 	t	\N	\N
27	Cultivo de melón	melones cantaloupe orgánicos, cultivo a cielo abierto, melones cantaloupe, cultivo a cielo abierto, melones gota de miel orgánicos, cultivo a cielo abierto, melones gota de miel, cultivo a cielo abierto, melones imperiales orgánicos, cultivo a cielo abierto, melones imperiales, cultivo a cielo abierto, melones laguna orgánicos, cultivo a cielo abierto, melones laguna, cultivo a cielo abierto, melones mixtos orgánicos, cultivo a cielo abierto, melones mixtos, cultivo a cielo abierto, melones orgá	t	\N	\N
28	Cultivo de tomate verde	costomate (tomate verde), cultivo a cielo abierto, costomate orgánico (tomate verde), cultivo a cielo abierto, dah-to (tomate verde), cultivo a cielo abierto, dah-to orgánico (tomate verde), cultivo a cielo abierto, miltomate (tomate verde), cultivo a cielo abierto, miltomate orgánico (tomate verde), cultivo a cielo abierto, tomates cimarrón (tomate verde), cultivo a cielo abierto, tomates cimarrón orgánicos (tomate verde), cultivo a cielo abierto, tomates de fresadilla (tomate verde), cultivo a	t	\N	\N
29	Cultivo de papa	papas alpha orgánicas, cultivo a cielo abierto, papas alpha, cultivo a cielo abierto, papas atlantic orgánicas, cultivo a cielo abierto, papas atlantic, cultivo a cielo abierto, papas cimarronas orgánicas, cultivo a cielo abierto, papas cimarronas, cultivo a cielo abierto, papas orgánicas, cultivo a cielo abierto, papas, cultivo a cielo abierto, papitas güeras orgánicas, cultivo a cielo abierto, papitas güeras, cultivo a cielo abierto	t	\N	\N
30	Cultivo de calabaza	ayojti orgánico, cultivo a cielo abierto, ayojti, cultivo a cielo abierto, calabacitas buttercup orgánicas, cultivo a cielo abierto, calabacitas buttercup, cultivo a cielo abierto, calabacitas chepi orgánicas, cultivo a cielo abierto, calabacitas chepi, cultivo a cielo abierto, calabacitas criollas orgánicas, cultivo a cielo abierto, calabacitas criollas, cultivo a cielo abierto, calabacitas de bola orgánicas, cultivo a cielo abierto, calabacitas de bola, cultivo a cielo abierto, calabacitas gra	t	\N	\N
31	Cultivo de sandía	sandías charleston orgánicas, cultivo a cielo abierto, sandías charleston, cultivo a cielo abierto, sandías orgánicas, cultivo a cielo abierto, sandías, cultivo a cielo abierto	t	\N	\N
32	Cultivo de otras hortalizas	acederas (hortalizas), cultivo a cielo abierto, acederas orgánicas (hortalizas), cultivo a cielo abierto, acelgas (hortalizas), cultivo a cielo abierto, acelgas orgánicas (hortalizas), cultivo a cielo abierto, achicorias (hortalizas), cultivo a cielo abierto, achicorias orgánicas (hortalizas), cultivo a cielo abierto, achira raíz (hortalizas), cultivo a cielo abierto, achira raíz orgánica (hortalizas), cultivo a cielo abierto, acocotes (hortalizas), cultivo a cielo abierto, acocotes orgánicos (h	t	\N	\N
114	Minería de manganeso	manganeso, beneficio, manganeso, explotación, manganeso, explotación integrada con las actividades de beneficio, manganeso, obtención de concentrados en la mina	t	\N	\N
33	Cultivo de naranja	naranjas agrias orgánicas, cultivo, naranjas agrias, cultivo, naranjas albérchiga orgánicas, cultivo, naranjas albérchiga, cultivo, naranjas cajera orgánicas, cultivo, naranjas cajera, cultivo, naranjas enanas orgánicas, cultivo, naranjas enanas, cultivo, naranjas fortuna orgánicas, cultivo, naranjas fortuna, cultivo, naranjas grey orgánicas, cultivo, naranjas grey, cultivo, naranjas injertadas orgánicas, cultivo, naranjas injertadas, cultivo, naranjas kunkuat orgánicas, cultivo, naranjas kunkua	t	\N	\N
34	Cultivo de limón	lima limón orgánico, cultivo, lima limón, cultivo, limoneros orgánicos, cultivo, limoneros, cultivo, limones agrios orgánicos, cultivo, limones agrios, cultivo, limones bear orgánicos, cultivo, limones bear, cultivo, limones canario orgánicos, cultivo, limones canario, cultivo, limones chinos orgánicos, cultivo, limones chinos, cultivo, limones cis orgánicos, cultivo, limones cis, cultivo, limones criollos orgánicos, cultivo, limones criollos, cultivo, limones indios orgánicos, cultivo, limones 	t	\N	\N
35	Cultivo de otros cítricos	cajerinas orgánicas, cultivo, cajerinas, cultivo, china lima orgánica, cultivo, china lima, cultivo, cidras orgánicas, cultivo, cidras, cultivo, cidros orgánicos, cultivo, cidros, cultivo, cultivo de diferentes cítricos cuando sea imposible determinar cuál es el principal, limas orgánicas, cultivo, limas, cultivo, limeros orgánicos, cultivo, limeros, cultivo, mandarinas orgánicas, cultivo, mandarinas, cultivo, mandarinos orgánicos, cultivo, mandarinos, cultivo, tangerinas orgánicas, cultivo, tan	t	\N	\N
36	Cultivo de café	café arábica orgánico, cultivo, café arábica, cultivo, café azteca orgánico, cultivo, café azteca, cultivo, café bourbon orgánico, cultivo, café bourbon, cultivo, café capulín orgánico, cultivo, café capulín, cultivo, café catimor orgánico, cultivo, café catimor, cultivo, café catohai orgánico, cultivo, café catohai, cultivo, café caturra orgánico, cultivo, café caturra, cultivo, café costa rica orgánico, cultivo, café costa rica, cultivo, café criollo orgánico, cultivo, café criollo, cultivo, c	t	\N	\N
37	Cultivo de plátano	bananos orgánicos, cultivo, bananos, cultivo, plátanos banano orgánicos, cultivo, plátanos banano, cultivo, plátanos bárbaros orgánicos, cultivo, plátanos bárbaros, cultivo, plátanos dominicos orgánicos, cultivo, plátanos dominicos, cultivo, plátanos enanos orgánicos, cultivo, plátanos enanos, cultivo, plátanos guineo orgánicos, cultivo, plátanos guineo, cultivo, plátanos machos orgánicos, cultivo, plátanos machos, cultivo, plátanos manzano orgánicos, cultivo, plátanos manzano, cultivo, plátanos	t	\N	\N
38	Cultivo de mango	mangos ataulfo orgánicos, cultivo, mangos ataulfo, cultivo, mangos criollos orgánicos, cultivo, mangos criollos, cultivo, mangos de manila orgánicos, cultivo, mangos de manila, cultivo, mangos haden orgánicos, cultivo, mangos haden, cultivo, mangos hayden orgánicos, cultivo, mangos hayden, cultivo, mangos heidi orgánicos, cultivo, mangos heidi, cultivo, mangos injertados orgánicos, cultivo, mangos injertados, cultivo, mangos keith orgánicos, cultivo, mangos keith, cultivo, mangos kensington orgá	t	\N	\N
39	Cultivo de aguacate	aguacachiles orgánicos, cultivo, aguacachiles, cultivo, aguacates cáscara delgada orgánicos, cultivo, aguacates cáscara delgada, cultivo, aguacates chinin orgánicos, cultivo, aguacates chinin, cultivo, aguacates criollos orgánicos, cultivo, aguacates criollos, cultivo, aguacates fuertes orgánicos, cultivo, aguacates fuertes, cultivo, aguacates hass orgánicos, cultivo, aguacates hass, cultivo, aguacates injertados orgánicos, cultivo, aguacates injertados, cultivo, aguacates laguneros orgánicos, c	t	\N	\N
40	Cultivo de uva	uvas bola dulce orgánicas, cultivo, uvas bola dulce, cultivo, uvas orgánicas, cultivo, uvas pasa orgánicas, cultivo, uvas pasa, cultivo, uvas, cultivo, vides orgánicas, cultivo, vides, cultivo	t	\N	\N
41	Cultivo de manzana	manzanas ácidas orgánicas, cultivo, manzanas ácidas, cultivo, manzanas california orgánicas, cultivo, manzanas california, cultivo, manzanas dobles rojas orgánicas, cultivo, manzanas dobles rojas, cultivo, manzanas golden orgánicas, cultivo, manzanas golden, cultivo, manzanas granny smith orgánicas, cultivo, manzanas granny smith, cultivo, manzanas injertadas orgánicas, cultivo, manzanas injertadas, cultivo, manzanas orgánicas, cultivo, manzanas red delicious orgánicas, cultivo, manzanas red del	t	\N	\N
42	Cultivo de cacao	cacao blanco orgánico, cultivo, cacao blanco, cultivo, cacao cimarrón orgánico, cultivo, cacao cimarrón, cultivo, cacao orgánico, cultivo, cacao volador orgánico, cultivo, cacao volador, cultivo, cacao, cultivo	t	\N	\N
43	Cultivo de coco	cayocos orgánicos, cultivo, cayocos, cultivo, chun-kuy orgánico, cultivo, chun-kuy, cultivo, cocos copra orgánicos, cultivo, cocos copra, cultivo, cocos de agua orgánicos, cultivo, cocos de agua, cultivo, cocos orgánicos, cultivo, cocos plumosos orgánicos, cultivo, cocos plumosos, cultivo, cocos, cultivo, coquitos de aceite orgánicos, cultivo, coquitos de aceite, cultivo, corozos orgánicos, cultivo, corozos, cultivo, palmeras orgánicas, cultivo, palmeras, cultivo	t	\N	\N
44	Cultivo de otros frutales no cítricos y de nueces	abrileñas (frutales no cítricos y nueces), cultivo, abrileñas orgánicas (frutales no cítricos y nueces), cultivo, acebuches (frutales no cítricos y nueces), cultivo, acebuches orgánicos (frutales no cítricos y nueces), cultivo, aceitunas (frutales no cítricos y nueces), cultivo, aceitunas orgánicas (frutales no cítricos y nueces), cultivo, acerolas (frutales no cítricos y nueces), cultivo, acerolas orgánicas (frutales no cítricos y nueces), cultivo, acerolos (frutales no cítricos y nueces), cult	t	\N	\N
45	Cultivo de jitomate en invernaderos y otras estructuras agrícolas protegidas	jitomates (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, jitomates bola orgánicos, cultivo en invernaderos y otras estructuras agrícolas protegidas., jitomates bola, cultivo en invernaderos y otras estructuras agrícolas protegidas, jitomates cherry orgánicos, cultivo en invernaderos y otras estructuras agrícolas protegidas, jitomates cherry, cultivo en invernaderos y otras estructuras agrícolas protegidas, jitomates hidropónicos, jitomates hidropónicos o	t	\N	\N
46	Cultivo de fresa en invernaderos y otras estructuras agrícolas protegidas	fresas (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, fresas orgánicas (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, fresas orgánicas, cultivo en invernaderos y otras estructuras agrícolas protegidas, fresas, cultivo en invernaderos y otras estructuras agrícolas protegidas	t	\N	\N
47	Cultivo de bayas (berries) en invernaderos y otras estructuras agrícolas protegidas, excepto fresas	arándanos (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, arándanos orgánicos (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, arándanos orgánicos, cultivo en invernaderos y otras estructuras agrícolas protegidas, arándanos, cultivo en invernaderos y otras estructuras agrícolas protegidas, frambuesas (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, frambuesas orgánicas (plántu	t	\N	\N
49	Cultivo de manzana en invernaderos y otras estructuras agrícolas protegidas	manzanas orgánicas, cultivo en invernaderos y otras estructuras agrícolas protegidas, manzanas, cultivo en invernaderos y otras estructuras agrícolas protegidas	t	\N	\N
50	Cultivo de pepino en invernaderos y otras estructuras agrícolas protegidas	pepinos (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, pepinos orgánicos (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, pepinos orgánicos, cultivo en invernaderos y otras estructuras agrícolas protegidas, pepinos, cultivo en invernaderos y otras estructuras agrícolas protegidas	t	\N	\N
51	Cultivo de otros productos alimenticios en invernaderos y otras estructuras agrícolas protegidas	acelgas orgánicas (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, acelgas orgánicas, cultivo en invernaderos y otras estructuras agrícolas protegidas, acelgas, cultivo en invernaderos y otras estructuras agrícolas protegidas, achicorias (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, achicorias orgánicas (plántula o plantita), cultivo en invernaderos y otras estructuras agrícolas protegidas, achicorias orgánicas, c	t	\N	\N
52	Floricultura a cielo abierto	abanicos (flores), cultivo a cielo abierto, abanicos orgánicos (flores), cultivo a cielo abierto, abrileñas (flores), cultivo a cielo abierto, abrileñas orgánicas (flores), cultivo a cielo abierto, achiras (flores), cultivo a cielo abierto, achiras orgánicas (flores), cultivo a cielo abierto, adelaidas (flores), cultivo a cielo abierto, adelaidas orgánicas (flores), cultivo a cielo abierto, agapandos (flores), cultivo a cielo abierto, agapandos orgánicos (flores), cultivo a cielo abierto, agerat	t	\N	\N
53	Floricultura en invernaderos y otras estructuras agrícolas protegidas	abanicos (flores), cultivo en invernaderos y otras estructuras agrícolas protegidas, abanicos orgánicos (flores), cultivo en invernaderos y otras estructuras agrícolas protegidas, abrileñas (flores), cultivo en invernaderos y otras estructuras agrícolas protegidas, abrileñas orgánicas (flores), cultivo en invernaderos y otras estructuras agrícolas protegidas, achiras (flores), cultivo en invernaderos y otras estructuras agrícolas protegidas, achiras orgánicas (flores), cultivo en invernaderos y 	t	\N	\N
54	Cultivo de árboles de ciclo productivo de 10 años o menos	acacias (árboles de ciclo productivo de 10 años o menos), cultivo en invernaderos y otras estructuras agrícolas protegidas, alacranes (árboles de ciclo productivo de 10 años o menos), cultivo en invernaderos y otras estructuras agrícolas protegidas, alcanfores (árboles de ciclo productivo de 10 años o menos), cultivo en invernaderos y otras estructuras agrícolas protegidas, árboles de especies maderables de ciclo productivo de 10 años o menos, cultivo en invernaderos y otras estructuras agrícola	t	\N	\N
55	Otros cultivos no alimenticios en invernaderos y otras estructuras agrícolas protegidas	Otros cultivos no alimenticios en invernaderos y otras estructuras agrícolas protegidas 	t	\N	\N
56	Cultivo de tabaco	may, cultivo, tabaco burley, cultivo, tabaco negro, cultivo, tabaco virginia, cultivo, tabaco, cultivo	t	\N	\N
57	Cultivo de algodón	algodón hueso, cultivo, algodón, cultivo	t	\N	\N
58	Cultivo de caña de azúcar	cañas (fruta), cultivo, cañas de azúcar, cultivo, cañas de java, cultivo, cañas para piloncillo, cultivo	t	\N	\N
59	Cultivo de alfalfa	alfalfa achicalada, cultivo, alfalfa berdiana, cultivo, alfalfa híbrida, cultivo, alfalfa mejorada, cultivo, alfalfa, cultivo, alfalfilla, cultivo	t	\N	\N
60	Cultivo de pastos	aceitilla para forraje (pastos o zacates), cultivo, alta fescue para forraje (pastos o zacates), cultivo, arúgula para forraje (pastos o zacates), cultivo, avenilla para forraje (pastos o zacates), cultivo, ballico para forraje (pastos o zacates), cultivo, bermudas para forraje (pastos o zacates), cultivo, braquianum para forraje (pastos o zacates), cultivo, braquiaria para forraje (pastos o zacates), cultivo, cadillo para forraje (pastos o zacates), cultivo, camelote para forraje (pastos o zaca	t	\N	\N
61	Cultivo de agaves alcoholeros	acambas (agaves alcoholeros), cultivo, agaves alcoholeros, cultivo, agaves azules, cultivo, agave bacanora, cultivo, aguamiel, obtención, cachú (agaves alcoholeros), cultivo, määxo (agaves alcoholeros), cultivo, magueyes mansos, cultivo, magueyes mezcaleros, cultivo, magueyes pulqueros, cultivo, magueyes tequileros, cultivo, teometl (agaves alcoholeros), cultivo	t	\N	\N
62	Cultivo de cacahuate	cacahuates bachimba-74, cultivo, cacahuates florida gigante, cultivo, cacahuates giorgia, cultivo, cacahuates guerrero-3, cultivo, cacahuates mixtecos, cultivo, cacahuates orgánicos, cultivo, cacahuates secos, cultivo, cacahuates virginia bunch, cultivo, cacahuates, cultivo, maní, cultivo	t	\N	\N
63	Actividades agrícolas combinadas con explotación de animales	actividades agrícolas combinadas con explotación de animales cuando sea imposible determinar cuál es la actividad principal	t	\N	\N
64	Actividades agrícolas combinadas con aprovechamiento forestal	actividades agrícolas combinadas con aprovechamiento forestal cuando sea imposible determinar cuál es la actividad principal	t	\N	\N
65	Actividades agrícolas combinadas con explotación de animales y aprovechamiento forestal	actividades agrícolas combinadas con explotación de animales y aprovechamiento forestal cuando sea imposible determinar cuál es la actividad principal	t	\N	\N
66	Otros cultivos	aak (fruto), cultivo, aak orgánico (fruto), cultivo, achicoria (savia), cultivo, achicorias orgánicas (savia), cultivo, achiote (fruto, tallo), cultivo, achiote orgánico (fruto, tallo), cultivo, acocotes (fruto), cultivo, acocotes orgánicos (fruto), cultivo, acoyos orgánicos, cultivo, acoyos, cultivo, acua'u orgánico, cultivo, acua'u, cultivo, agave para la obtención de fibras textiles, cultivo, ajenjo (hojas), cultivo, ajenjo orgánico (hojas), cultivo, alachis orgánico, cultivo, alachis, cultiv	t	\N	\N
67	Explotación de bovinos para la producción de carne	becerras, cría para ser utilizadas como ganado bovino lechero, becerros, explotación para la producción de carne, beefalos, explotación para la producción de carne, bisontes, explotación para la producción de carne, bovinos cebús, explotación para la producción de carne, bovinos, explotación para la producción de carne, búfalos de agua, explotación para la producción de carne, crías bovinas, explotación para la producción de carne, crías de búfalo, explotación para la producción de carne, katalo	t	\N	\N
68	Explotación de bovinos para la producción de leche	bovinos cebús, explotación para la producción de leche, bovinos, explotación para la producción de leche, bovinos, explotación para la producción de leche orgánica, pies de cría de bovinos cebús, explotación para la producción de leche, pies de cría de bovinos, explotación para la producción de leche, sementales bovinos, explotación para la producción de leche, vacas, explotación para la producción de leche, vaquillas, explotación para la producción de leche, vientres bovinos, explotación para l	t	\N	\N
69	Explotación de bovinos para la producción conjunta de leche y carne	becerras, explotación para la producción conjunta de leche y carne, becerros, explotación para la producción conjunta de leche y carne, bovinos cebús, explotación para la producción conjunta de leche y carne, bovinos, explotación para la producción conjunta de leche no orgánica y carne, bovinos, explotación para la producción conjunta de leche orgánica y carne, crías bovinas, explotación para la producción conjunta de leche y carne, crías de ganado bovino cebú, explotación para la producción con	t	\N	\N
70	Explotación de bovinos para otros propósitos	bovinos cebús para trabajo, explotación, bovinos para jaripeos y rodeos, explotación, bovinos para trabajo, explotación, bueyes para trabajo, explotación, explotación de ganado bovino con diferentes propósitos cuando sea imposible determinar cuál es el principal, ganado bovino para deporte, explotación, ganado bovino para esparcimiento, explotación, toros de lidia, explotación	t	\N	\N
71	Explotación de porcinos en granja	cerdos, explotación en granjas, cochicuinos, explotación en granjas, crías de ganado porcino, explotación en granjas, lechones, explotación en granjas, marranas no vientre, explotación en granjas, marranas vientre, explotación en granjas, pies de cría de ganado porcino, explotación en granjas, sementales porcinos, explotación en granjas	t	\N	\N
72	Explotación de porcinos en traspatio	cerdos, explotación en traspatio, cochicuinos, explotación en traspatio, crías de ganado porcino, explotación en traspatio, lechones, explotación en traspatio, marranas no vientre, explotación en traspatio, marranas vientre, explotación en traspatio, pies de cría de ganado porcino, explotación en traspatio, sementales porcinos, explotación en traspatio	t	\N	\N
73	Explotación de gallinas para la producción de huevo fértil	gallinas abuelas, explotación para la producción de huevo fértil, gallinas ancona, explotación para la producción de huevo fértil, gallinas arbor acres, explotación para la producción de huevo fértil, gallinas de postura, explotación para la producción de huevo fértil, gallinas leghorn, explotación para la producción de huevo fértil, gallinas madre, explotación para la producción de huevo fértil, gallinas minorca, explotación para la producción de huevo fértil, gallinas new hampshire, explotació	t	\N	\N
74	Explotación de gallinas para la producción de huevo para plato	gallinas abuela, explotación para la producción de huevo para plato, gallinas ancona, explotación para la producción de huevo para plato, gallinas arbor acres, explotación para la producción de huevo para plato, gallinas de postura, explotación para la producción de huevo para plato, gallinas leghorn, explotación para la producción de huevo para plato, gallinas minorca, explotación para la producción de huevo para plato, gallinas new hampshire, explotación para la producción de huevo para plato,	t	\N	\N
75	Explotación de pollos para la producción de carne	engorda de pollos para la producción de carne, gallos rhode island red, explotación para la producción de carne, pollas, explotación para la producción de carne, pollos con pluma, explotación para la producción de carne, pollos de engorda, explotación para la producción de carne, pollos sin pluma, explotación para la producción de carne, pollos, explotación para la producción de carne	t	\N	\N
76	Explotación de guajolotes o pavos	coquenas, explotación para la producción de carne y huevo, corucos, explotación para la producción de carne y huevo, guajolotes, explotación para la producción de carne y huevo, guilos, explotación para la producción de carne y huevo, konitos, explotación para la producción de carne y huevo, pavas, explotación para la producción de carne y huevo, paveznos, explotación para la producción de carne y huevo, pavipollos, explotación para la producción de carne y huevo, pies de cría de guajolote, expl	t	\N	\N
77	Producción de aves en incubadora	aves, producción en incubadora, pollitas de gallina de huevo para plato, producción en incubadora, pollitas de gallina para postura, producción en incubadora, pollitas de gallina, producción en incubadora, pollitas de gallinas reproductoras, producción en incubadora, pollitos de avestruz, producción en incubadora, pollitos de engorda, producción en incubadora, pollitos de faisán, producción en incubadora, pollitos de guajolote, producción en incubadora, pollitos de un día, producción en incubado	t	\N	\N
78	Explotación de otras aves para producción de carne y huevo	aves, explotación para producción de carne y huevo, avestruces, explotación para producción de carne y huevo, codornices, explotación para producción de carne y huevo, emúes, explotación para producción de carne y huevo, explotación de diferentes tipos de aves en cualquiera de sus fases para la producción de carne y huevo cuando sea imposible determinar cuál es la actividad principal, faisanes, explotación para producción de carne y huevo, gansos, explotación para producción de carne y huevo, pa	t	\N	\N
79	Explotación de ovinos	carneros, explotación, explotación combinada de ovinos con caprinos cuando sea imposible determinar cuál es la actividad principal, ganado ovino para carne y leche, explotación, ganado ovino para carne, explotación, muflones, explotación, ovejas de lana en producción, explotación, ovejas de lana reproductoras, explotación, ovejas de lana, explotación, ovejas reproductoras, explotación, ovinos para rastro, explotación, pies de cría de ovinos, explotación, sementales ovinos, explotación, vientres 	t	\N	\N
80	Explotación de caprinos	cabras en desarrollo, explotación, cabras hembras de carne, explotación, cabras hembras de leche, explotación, cabras machos de carne, explotación, cabras machos de leche, explotación, cabras, explotación, cabritos de carne, explotación, cabritos de leche, explotación, caprinos, explotación, chivatos de carne, explotación, chivatos de leche, explotación, chivatos, explotación, pies de cría de caprinos de carne, explotación, pies de cría de caprinos de leche, explotación, pies de cría de caprinos	t	\N	\N
81	Camaronicultura y acuicultura de otros crustáceos en agua salada	acamayas de agua salada, cultivo y cría en ambientes controlados, acociles de agua salada, cultivo y cría en ambientes controlados, bogavantes de agua salada, cultivo y cría en ambientes controlados, bueyes de agua salada, cultivo y cría en ambientes controlados, camarones alevines de agua salada, cultivo y cría en ambientes controlados, camarones blancos del pacífico de agua salada, cultivo y cría en ambientes controlados, camarones cafés de agua salada, cultivo y cría en ambientes controlados,	t	\N	\N
82	Camaronicultura y acuicultura de otros crustáceos en agua dulce	acociles de agua dulce, cultivo y cría en ambientes controlados, camarones alevines de agua dulce, cultivo y cría en ambientes controlados, camarones blancos del pacífico de agua dulce, cultivo y cría en ambientes controlados, camarones cafés de agua dulce, cultivo y cría en ambientes controlados, camarones de agua dulce, cultivo y cría en ambientes controlados, cangrejos de agua dulce, cultivo y cría en ambientes controlados, crustáceos de agua dulce, cultivo y cría en ambientes controlados, la	t	\N	\N
83	Piscicultura en agua dulce	ajolotes de agua dulce, cultivo y cría en ambientes controlados, alevines de peces de agua dulce, cultivo y cría en ambientes controlados, ángeles (peces) de agua dulce, cultivo y cría en ambientes controlados, apaiaris de agua dulce, cultivo y cría en ambientes controlados, bagres alevines de agua dulce, cultivo y cría en ambientes controlados, bagres de agua dulce, cultivo y cría en ambientes controlados, bagres de canal de agua dulce, cultivo y cría en ambientes controlados, barbos de agua du	t	\N	\N
84	Piscicultura en agua salada	alevines de peces marinos, cultivo y cría en ambientes controlados, atunes aleta azul de agua salada, cultivo y cría en ambientes controlados, atunes de agua salada, cultivo y cría en ambientes controlados, cirujanos azules (peces) de agua salada, cultivo y cría en ambientes controlados, cirujanos pardos (peces) de agua salada, cultivo y cría en ambientes controlados, cirujanos rayados (peces) de agua salada, cultivo y cría en ambientes controlados, cojinudas de agua salada, cultivo y cría en am	t	\N	\N
85	Otra acuicultura	acuicultura vegetal, algas, acuicultura vegetal, almejas arca auriculadas, cultivo y cría en ambientes controlados, almejas arca zebra, cultivo y cría en ambientes controlados, almejas blancas, cultivo y cría en ambientes controlados, almejas chocolatas, cultivo y cría en ambientes controlados, almejas negras, cultivo y cría en ambientes controlados, almejas rosadas, cultivo y cría en ambientes controlados, almejas, cultivo y cría en ambientes controlados, anfibios, cultivo y cría en ambientes c	t	\N	\N
86	Apicultura	abejas para miel, explotación, recolección y venta, abejas para veneno, explotación, recolección y venta, abejas reinas, explotación, recolección y venta, apiarios, explotación y venta, apicultura (explotación de abejas), cera de abejas, recolección y venta, cera en greña, recolección y venta, colmenas rústicas, explotación y venta, colmenas tecnificadas, explotación y venta, colmenas, explotación y venta, jalea real de abeja, recolección y venta, miel de colmena, recolección y venta, miel orgán	t	\N	\N
87	Explotación de équidos	acémilas, explotación, burdéganos, explotación, burras para leche, explotación, burras reproductoras, explotación, burritos, explotación, burro para carne, explotación, burros, explotación, caballos de carreras, explotación, caballos para carne, explotación, caballos para criadero, explotación, caballos para deporte, explotación, caballos para pelo o crin, explotación, caballos para salto, explotación, caballos para trabajo, explotación, caballos poni, explotación, caballos pura sangre, explotac	t	\N	\N
88	Cunicultura y explotación de animales con pelaje fino	animales con pelaje fino, explotación en ambientes controlados, chinchilla para piel, explotación en ambientes controlados, conejo de angora, explotación en ambientes controlados, conejo para pelo, explotación en ambientes controlados, cunicultura (explotación de conejos), nutria para piel, explotación en ambientes controlados, vientre de animales con pelaje fino, explotación en ambientes controlados, vientre de chinchilla, explotación en ambientes controlados, vientre de conejo, explotación en 	t	\N	\N
89	Explotación de animales combinada con aprovechamiento forestal	actividades de explotación de animales combinadas con aprovechamiento forestal cuando sea imposible determinar cuál es la actividad principal	t	\N	\N
90	Explotación de otros animales	águilas reales, explotación en ambientes controlados, alacranes criados para veneno, explotación en ambientes controlados, alacranes, explotación en ambientes controlados, alces, explotación en ambientes controlados, animales de laboratorio, explotación en ambientes controlados, arañas criadas para veneno, explotación en ambientes controlados, arañas, explotación en ambientes controlados, aves cantoras, explotación en ambientes controlados, aves de ornato, explotación en ambientes controlados, a	t	\N	\N
91	Silvicultura	acebuches (especies maderables de ciclos productivos mayores de 10 años), cultivo, algarrobos (especies maderables de ciclos productivos mayores de 10 años), cultivo, algodoncillos (especies maderables de ciclos productivos mayores de 10 años), cultivo, cacahuananches (especies maderables de ciclos productivos mayores de 10 años), cultivo, caobas (especies maderables de ciclos productivos mayores de 10 años), cultivo, carneros (especies maderables de ciclos productivos mayores de 10 años), culti	t	\N	\N
92	Viveros forestales	abedules (especie forestal), cultivo para forestación y reforestación, abetos (especie forestal), cultivo para forestación y reforestación, abib (especie forestal), cultivo para forestación y reforestación, abutilones (especie forestal), cultivo para forestación y reforestación, acacias (especie forestal), cultivo para forestación y reforestación, acalamas (especie forestal), cultivo para forestación y reforestación, acebuches (especie forestal), cultivo para forestación y reforestación, aceitil	t	\N	\N
93	Recolección de productos forestales	Recolección de productos forestales 	t	\N	\N
94	Aprovechamiento de árboles	abalos (árboles), aprovechamiento de árboles, abetos (árboles), aprovechamiento de árboles, abib (árboles), aprovechamiento de árboles, abiodos (árboles), aprovechamiento de árboles, abutilones (árboles), aprovechamiento de árboles, acacias (árboles), aprovechamiento de árboles, acahuales (árboles), aprovechamiento de árboles, acalocotes (árboles), aprovechamiento de árboles, acalotes (árboles), aprovechamiento de árboles, acebuches (árboles), aprovechamiento de árboles, achiote (árboles), aprov	t	\N	\N
95	Pesca de camarón	camarines, pesca de, camarones alevines, pesca, camarones azules, pesca, camarones blancos del Pacífico, pesca, camarones blancos, pesca, camarones botalón, pesca, camarones burro, pesca, camarones cacahuate, pesca, camarones cafés, pesca, camarones cebra, pesca, camarones cristal, pesca, camarones cristalinos, pesca, camarones de agua dulce, pesca, camarones de piedra, pesca, camarones de río, pesca, camarones de roca, pesca, camarones japoneses, pesca, camarones kaki, pesca, camarones mezclill	t	\N	\N
96	Pesca de túnidos	albacoras (túnidos), pesca, atunes aleta amarilla, pesca, atunes aleta azul, pesca, atunes aleta negra, pesca, atunes blancos, pesca, atunes de aletas largas, pesca, atunes obesos, pesca, atunes ojigrandes, pesca, atunes, pesca, bacoretas (túnidos), pesca, barriletes (túnidos), pesca, bonitos (túnidos), pesca, caballas (túnidos), pesca, cachorras (túnidos), pesca, cachorretas (túnidos), pesca, cachurretas (túnidos), pesca, carachanas pintadas (túnidos), pesca, carites (túnidos), pesca, caritos (	t	\N	\N
97	Pesca de sardina y anchoveta	anchoas, pesca, anchovetas, pesca, arenques (sardina o anchoveta), pesca, boconas (sardina o anchoveta), pesca, boquerones (sardina o anchoveta), pesca, manjúas (sardina o anchoveta), pesca, peces rey (sardina o anchoveta), pesca, sardinas boconas, pesca, sardinas carapachonas, pesca, sardinas crinudas, pesca, sardinas de escama fina, pesca, sardinas del Pacífico, pesca, sardinas escamudas, pesca, sardinas japonesas, pesca, sardinas lachas, pesca, sardinas machete, pesca, sardinas Monterrey, pes	t	\N	\N
98	Pesca y captura de otros peces, crustáceos, moluscos y otras especies	abadejos, pesca, extracción y captura, abulones, pesca, extracción y captura, acamayas, pesca, extracción y captura, acociles, pesca, extracción y captura, agallas azules, pesca, extracción y captura, aguajíes, pesca, extracción y captura, aguamalas, pesca, extracción y captura, aguavinas, pesca, extracción y captura, agujas, pesca, extracción y captura, agujones, pesca, extracción y captura, ajolotes, pesca, extracción y captura, alabatos, pesca, extracción y captura, albatos, pesca, extracción	t	\N	\N
99	Caza y captura	administración de reservas para caza, animales en su hábitat natural, caza y captura, caza y captura de animales en ranchos cinegéticos, operación de reservas para caza	t	\N	\N
100	Servicios de fumigación agrícola	fumigación agrícola, servicios	t	\N	\N
101	Despepite de algodón	algodón pluma, despepite, algodón, despepite	t	\N	\N
102	Beneficio de productos agrícolas	aireado de productos agrícolas (excepto arroz, cacao, café, tabaco y algodón), beneficio de productos agrícolas (excepto arroz, cacao, café, tabaco y algodón), descascarado de productos agrícolas (excepto arroz, cacao, café, tabaco y algodón), empacado de productos agrícolas (excepto arroz, cacao, café, tabaco y algodón), encerado de productos agrícolas (excepto arroz, cacao, café, tabaco y algodón), etiquetado de productos agrícolas (excepto arroz, cacao, café, tabaco y algodón), limpieza de pr	t	\N	\N
103	Otros servicios relacionados con la agricultura	administración de granjas agrícolas, administración de unidades económicas agrícolas, colocación de personal agrícola, servicios, cosecha, servicios, curado de productos agrícolas, servicios, desgrane de productos agrícolas, servicios, equipo de uso agrícola con operador, alquiler, fertilización de suelos para la agricultura, servicios, maquinaria y equipo de uso agrícola con operador, alquiler, poda de árboles frutales, servicios para la agricultura, preparación de suelos para la agricultura, s	t	\N	\N
104	Servicios relacionados con la cría y explotación de animales	administración de granjas ganaderas, administración de unidades económicas ganaderas, albergue de ganado, servicios, albergue y cuidado de ganado, servicios, bancos de esperma animal, servicios, bancos de sangre para la ganadería, servicios, baños parasiticidas, servicios, báscula para ganado, servicios, castración del ganado, servicios, clasificación de huevo, servicios, cruza de ganado, servicios, cuidado de ganado, servicios, herraje de caballos, servicios, herraje de ganado, servicios, insem	t	\N	\N
105	Servicios relacionados con el aprovechamiento forestal	aclareo de productos silvícolas, servicios, administración de unidades económicas forestales, control de inventarios de existencias maderables, servicios, control de plagas y enfermedades de productos silvícolas, servicios, maquinaria y equipo de uso forestal con operador, alquiler, poda de productos silvícolas, servicios, reforestación de productos silvícolas, servicios, selección de productos silvícolas, servicios	t	\N	\N
106	Extracción de petróleo y gas natural asociado	gas natural asociado, extracción en campos petroleros, petróleo condensado, extracción, petróleo crudo amargo mediano, extracción, petróleo crudo amargo, extracción, petróleo crudo de arenas alquitranadas, extracción, petróleo crudo de arenas bituminosas, extracción, petróleo crudo de esquistos bituminosos, extracción, petróleo crudo dulce ligero, extracción, petróleo crudo dulce, extracción, petróleo crudo ligero, extracción, petróleo crudo liviano, extracción, petróleo crudo mediano, extracció	t	\N	\N
107	Extracción de gas natural no asociado	azufre del gas natural, obtención en campos de gas natural, condensados del gas natural, obtención en campos de gas natural, gas butano natural, obtención en campos de gas natural, gas etano natural, obtención en campos de gas natural, gas metano, obtención en campos de gas natural, gas natural Licuado de Petróleo (L. P.), obtención en campos de gas natural, gas natural líquido condensado, extracción en campos de gas natural, gas natural no asociado, absorción en campos de gas natural, gas natur	t	\N	\N
108	Minería de carbón mineral	antracita, beneficio, antracita, explotación, antracita, explotación integrada con las actividades de beneficio, carbón bituminoso, beneficio, carbón bituminoso, explotación, carbón bituminoso, explotación integrada con las actividades de beneficio, carbón de vapor subbituminoso, beneficio, carbón de vapor subbituminoso, explotación, carbón de vapor subbituminoso, explotación integrada con las actividades de beneficio, carbón fósil, beneficio, carbón fósil, explotación, carbón fósil, explotación	t	\N	\N
109	Minería de hierro	hematita, beneficio, hematita, explotación, hematita, explotación integrada con las actividades de beneficio, hematita, obtención de concentrados en la mina, hierro en briquetas, beneficio, hierro, beneficio, hierro, explotación, hierro, explotación integrada con las actividades de beneficio, hierro, obtención de concentrados en la mina, limonita, beneficio, limonita, explotación, limonita, explotación integrada con las actividades de beneficio, magnetita, beneficio, magnetita, explotación, magn	t	\N	\N
110	Minería de oro	calaverita, beneficio, calaverita, explotación, calaverita, explotación integrada con las actividades de beneficio, oro, beneficio, oro, explotación, oro, explotación integrada con las actividades de beneficio, oro, obtención de concentrados en la mina, plantas de beneficio de oro, silvanita, beneficio para la obtención de oro, silvanita, explotación integrada con las actividades de beneficio para la obtención de oro, silvanita, explotación para la obtención de oro, telururos, beneficio para la 	t	\N	\N
111	Minería de plata	plantas de beneficio de plata, plata, beneficio, plata, explotación, plata, explotación integrada con las actividades de beneficio, plata, obtención de concentrados en la mina, silvanita, beneficio para la obtención de plata, silvanita, explotación integrada con las actividades de beneficio para la obtención de plata, silvanita, explotación para la obtención de plata, telurita, beneficio, telurita, explotación, telurita, explotación integrada con las actividades de beneficio, telururos, benefici	t	\N	\N
112	Minería de cobre	calcocita, beneficio, calcocita, explotación, calcocita, explotación integrada con las actividades de beneficio, cobre, beneficio, cobre, explotación, cobre, explotación integrada con las actividades de beneficio, cobre, extracción por solventes y depositación electrolítica, cobre, obtención de concentrados en la mina, cuprita, beneficio, cuprita, explotación, cuprita, explotación integrada con las actividades de beneficio, níquel, beneficio, níquel, explotación, níquel, explotación integrada co	t	\N	\N
113	Minería de plomo y zinc	calamina, beneficio, calamina, explotación, calamina, explotación integrada con las actividades de beneficio, calcopirita, beneficio, calcopirita, explotación, calcopirita, explotación integrada con las actividades de beneficio, cerusita, beneficio, cerusita, explotación, cerusita, explotación integrada con las actividades de beneficio, esfalerita, beneficio, esfalerita, explotación, esfalerita, explotación integrada con las actividades de beneficio, esmitsonita, beneficio, esmitsonita, explotac	t	\N	\N
115	Minería de mercurio y antimonio	antimonio, beneficio, antimonio, explotación, antimonio, explotación integrada con las actividades de beneficio, antimonio, obtención de concentrados en la mina, mercurio, beneficio, mercurio, explotación, mercurio, explotación integrada con las actividades de beneficio, mercurio, obtención de concentrados en la mina	t	\N	\N
116	Minería de uranio y minerales radiactivos	actinio, beneficio, actinio, explotación, actinio, explotación integrada con las actividades de beneficio, carnotita, beneficio, carnotita, explotación, carnotita, explotación integrada con las actividades de beneficio, itrio, beneficio, itrio, explotación, itrio, explotación integrada con las actividades de beneficio, itrio, obtención de concentrados en la mina, minerales radiactivos, beneficio, minerales radiactivos, explotación, minerales radiactivos, explotación integrada con las actividades	t	\N	\N
117	Minería de otros minerales metálicos	bastnasita, beneficio, bastnasita, explotación, bastnasita, explotación integrada con las actividades de beneficio, bauxita, beneficio, bauxita, explotación, bauxita, explotación integrada con las actividades de beneficio, berilio, beneficio, berilio, explotación, berilio, explotación integrada con las actividades de beneficio, berilio, obtención de concentrados en la mina, cerio, beneficio, cerio, explotación, cerio, explotación integrada con las actividades de beneficio, cerio, obtención de co	t	\N	\N
118	Minería de piedra caliza	carbonato de calcio, beneficio, carbonato de calcio, explotación, carbonato de calcio, explotación integrada con las actividades de beneficio, creta, beneficio, creta, explotación, creta, explotación integrada con las actividades de beneficio, dolomita, beneficio, dolomita, explotación, dolomita, explotación integrada con las actividades de beneficio, marga, beneficio, marga, explotación, marga, explotación integrada con las actividades de beneficio, piedra caliza bituminosa, beneficio, piedra c	t	\N	\N
119	Minería de mármol	diorita, beneficio, diorita, explotación, diorita, explotación integrada con las actividades de beneficio, gneis, beneficio, gneis, explotación, gneis, explotación integrada con las actividades de beneficio, granito metalúrgico, beneficio, granito metalúrgico, explotación, granito metalúrgico, explotación integrada con las actividades de beneficio, granito, beneficio, granito, explotación, granito, explotación integrada con las actividades de beneficio, mármol brecha, beneficio, mármol brecha, e	t	\N	\N
120	Minería de otras piedras dimensionadas	basalto, beneficio, basalto, explotación, basalto, explotación integrada con las actividades de beneficio, cuarcita, beneficio, cuarcita, explotación, cuarcita, explotación integrada con las actividades de beneficio, diabasa, beneficio, diabasa, explotación, diabasa, explotación integrada con las actividades de beneficio, gabro, beneficio, gabro, explotación, gabro, explotación integrada con las actividades de beneficio, ganister, beneficio, ganister, explotación, ganister, explotación integrada	t	\N	\N
121	Minería de arena y grava para la construcción	arena abrasiva, beneficio, arena abrasiva, explotación, arena abrasiva, explotación integrada con las actividades de beneficio, arena común, beneficio, arena común, explotación, arena común, explotación integrada con las actividades de beneficio, arena de moldeo, beneficio, arena de moldeo, explotación, arena de moldeo, explotación integrada con las actividades de beneficio, arena gruesa, beneficio, arena gruesa, explotación, arena gruesa, explotación integrada con las actividades de beneficio, 	t	\N	\N
122	Minería de tezontle y tepetate	tepetate, beneficio, tepetate, explotación, tepetate, explotación integrada con las actividades de beneficio, tezontle, beneficio, tezontle, explotación, tezontle, explotación integrada con las actividades de beneficio	t	\N	\N
123	Minería de feldespato	albita, beneficio, albita, explotación, albita, explotación integrada con las actividades de beneficio, anortita, beneficio, anortita, explotación, anortita, explotación integrada con las actividades de beneficio, feldespato, beneficio, feldespato, explotación, feldespato, explotación integrada con las actividades de beneficio, ortosa, beneficio, ortosa, explotación, ortosa, explotación integrada con las actividades de beneficio, pegmatita, beneficio, pegmatita, explotación, pegmatita, explotaci	t	\N	\N
124	Minería de sílice	arena sílica, beneficio, arena sílica, explotación, arena sílica, explotación integrada con las actividades de beneficio, coesita, beneficio, coesita, explotación, coesita, explotación integrada con las actividades de beneficio, cristobalita, beneficio, cristobalita, explotación, cristobalita, explotación integrada con las actividades de beneficio, cuarzo, beneficio, cuarzo, explotación, cuarzo, explotación integrada con las actividades de beneficio, melanoflogita, beneficio, melanoflogita, expl	t	\N	\N
125	Minería de caolín	caolín, beneficio, caolín, explotación, caolín, explotación integrada con las actividades de beneficio	t	\N	\N
126	Minería de otras arcillas y de otros minerales refractarios	andalucita, beneficio, andalucita, explotación, andalucita, explotación integrada con las actividades de beneficio, aplita, beneficio, aplita, explotación, aplita, explotación integrada con las actividades de beneficio, arcillas de uso industrial, beneficio, arcillas de uso industrial, explotación, arcillas de uso industrial, explotación integrada con las actividades de beneficio, arcillas no refractarias, beneficio, arcillas no refractarias, explotación, arcillas no refractarias, explotación in	t	\N	\N
127	Minería de sal	sal, beneficio, sal, explotación, sal, explotación integrada con las actividades de beneficio	t	\N	\N
128	Minería de piedra de yeso	yeso, beneficio, yeso, explotación, yeso, explotación integrada con las actividades de beneficio	t	\N	\N
129	Minería de barita	barita, beneficio, barita, explotación, barita, explotación integrada con las actividades de beneficio, barita, obtención de concentrados en la mina, baritina, beneficio, baritina, explotación, baritina, explotación integrada con las actividades de beneficio	t	\N	\N
130	Minería de roca fosfórica	roca fosfórica, beneficio, roca fosfórica, explotación, roca fosfórica, explotación integrada con las actividades de beneficio	t	\N	\N
131	Minería de fluorita	fluorita, beneficio, fluorita, explotación, fluorita, explotación integrada con las actividades de beneficio	t	\N	\N
132	Minería de grafito	grafito, beneficio, grafito, explotación, grafito, explotación integrada con las actividades de beneficio	t	\N	\N
133	Minería de azufre	azufre, beneficio, azufre, explotación, azufre, explotación integrada con las actividades de beneficio	t	\N	\N
134	Minería de minerales no metálicos para productos químicos	alunita o piedra de alumbre, beneficio, alunita o piedra de alumbre, explotación, alunita o piedra de alumbre, explotación integrada con las actividades de beneficio, arsénico, beneficio, arsénico, explotación, arsénico, explotación integrada con las actividades de beneficio, bloedita, beneficio, bloedita, explotación, bloedita, explotación integrada con las actividades de beneficio, boratos naturales, beneficio, boratos naturales, explotación, boratos naturales, explotación integrada con las ac	t	\N	\N
135	Minería de otros minerales no metálicos	abrasivos bituminosos, beneficio, abrasivos bituminosos, explotación, abrasivos bituminosos, explotación integrada con las actividades de beneficio, abrasivos naturales, beneficio, abrasivos naturales, explotación, abrasivos naturales, explotación integrada con las actividades de beneficio, ágata, beneficio, ágata, explotación, ágata, explotación integrada con las actividades de beneficio, alabastro, beneficio, alabastro, explotación, alabastro, explotación integrada con las actividades de benef	t	\N	\N
136	Perforación de pozos petroleros y de gas	acidificación por contrato de pozos de petróleo y gas, ademado por contrato de pozos de petróleo y gas, barrenado y voladura por contrato en campos petroleros y de gas natural, cableado por contrato en campos petroleros y de gas natural, cementación por contrato de pozos de petróleo y gas, desmantelamiento por contrato de aparejos en campos petroleros y de gas natural, desmantelamiento por contrato de pozos de petróleo, desmantelamiento por contrato de tanques de petróleo y gas, desmantelamiento	t	\N	\N
137	Otros servicios relacionados con la minería	bombeo por contrato de minas, bombeo por contrato de minas de carbón, bombeo por contrato de minas de minerales metálicos, bombeo por contrato de minas de minerales no metálicos, dragado por contrato de minas, dragado por contrato de minas de carbón, dragado por contrato de minas de minerales metálicos, dragado por contrato de minas de minerales no metálicos, drenado por contrato de minas, drenado por contrato de minas de carbón, drenado por contrato de minas de minerales metálicos, drenado por 	t	\N	\N
138	Generación de electricidad a partir de combustibles fósiles	energía eléctrica proveniente de combustibles fósiles (carbón, petróleo y gas), generación, energía eléctrica proveniente de plantas carboeléctricas, generación	t	\N	\N
139	Generación de electricidad a partir de energía hidráulica	energía eléctrica proveniente de plantas hidroeléctricas, generación, energía hidroeléctrica, generación	t	\N	\N
140	Generación de electricidad a partir de energía solar	energía eléctrica solar, generación	t	\N	\N
141	Generación de electricidad a partir de energía eólica	energía eléctrica proveniente de estructuras de energía eólica, generación	t	\N	\N
142	Generación de electricidad a partir de otro tipo de energía	energía eléctrica mareomotriz, generación, energía eléctrica proveniente de plantas geotérmicas, generación, energía eléctrica proveniente de plantas nucleares, generación, energía eléctrica proveniente de plantas nucleoeléctricas, generación, energía eléctrica proveniente de plantas termoeléctricas, generación	t	\N	\N
143	Transmisión de energía eléctrica	energía eléctrica, transmisión	t	\N	\N
144	Distribución de energía eléctrica	energía eléctrica, distribución	t	\N	\N
145	Comercialización de energía eléctrica	energía eléctrica, comercialización, energía eléctrica, suministro	t	\N	\N
146	Suministro de gas natural por ductos al consumidor final	aire caliente, suministro por ductos, aire frío, suministro por ductos, combustibles gaseosos, distribución por ductos al consumidor final, gas a usuarios comerciales, suministro por ductos, gas a usuarios industriales, suministro por ductos, gas a usuarios residenciales, suministro por ductos, gas natural, distribución por ductos, gas por ductos al consumidor final, vapor para calefacción, distribución por ductos, vapor para energía, distribución por ductos, vapor por ductos, producción, captac	t	\N	\N
147	Captación, tratamiento y suministro de agua realizados por el sector privado	agua de manantiales, captación por parte del sector privado, agua de pozo, captación por parte del sector privado, agua de presas, captación por parte del sector privado, agua de ríos, captación por parte del sector privado, agua potable, suministro en pipas por parte del sector privado, agua potable, suministro por parte del sector privado, agua, captación por parte del sector privado, agua, tratamiento para potabilización por parte del sector privado, aguas residuales, captación por parte del 	t	\N	\N
148	Captación, tratamiento y suministro de agua realizados por el sector público	agua de manantiales, captación por parte del sector público, agua de pozo, captación por parte del sector público, agua de presas, captación por parte del sector público, agua de ríos, captación por parte del sector público, agua potable, suministro en pipas por parte del sector público, agua potable, suministro por parte del sector público, agua, captación por parte del sector público, agua, tratamiento para potabilización por parte del sector público, aguas residuales, captación por parte del 	t	\N	\N
149	Edificación de vivienda unifamiliar	casas de campo, construcción, casas modulares unifamiliares, montaje en el sitio, casas panelizadas unifamiliares, montaje en el sitio, casas precortadas unifamiliares, montaje en el sitio, casas prefabricadas unifamiliares, montaje en el sitio, condominios horizontales unifamiliares, construcción, residencias unifamiliares, ampliación, remodelación, mantenimiento o reparación de la obra, residencias unifamiliares, construcción, vivienda de interés social unifamiliar, construcción, vivienda popu	t	\N	\N
150	Edificación de vivienda multifamiliar	casas dúplex, construcción, casas modulares multifamiliares, montaje en el sitio, casas panelizadas multifamiliares, montaje en el sitio, casas precortadas multifamiliares, montaje en el sitio, casas prefabricadas multifamiliares, montaje en el sitio, condominios de tiempo compartido, construcción, condominios, construcción, edificios de apartamentos, construcción, residencias multifamiliares, ampliación, remodelación, mantenimiento o reparación de la obra, residencias multifamiliares, construcc	t	\N	\N
151	Supervisión de edificación residencial	construcción de vivienda residencial multifamiliar, supervisión, construcción de vivienda residencial unifamiliar, supervisión, construcción residencial, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de vivienda residencial multifamiliar, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de vivienda residencial unifamiliar	t	\N	\N
152	Edificación de naves y plantas industriales, excepto la supervisión	agroindustrias (edificios), ampliación, remodelación, mantenimiento o reparación de la obra, agroindustrias (edificios), construcción, altos hornos, ampliación, remodelación, mantenimiento o reparación de la obra, altos hornos, construcción, aserraderos, ampliación, remodelación, mantenimiento o reparación de la obra, aserraderos, construcción, complejos siderúrgicos, ampliación, remodelación, mantenimiento o reparación de la obra, complejos siderúrgicos, construcción, embutidoras de carnes, amp	t	\N	\N
153	Supervisión de edificación de naves y plantas industriales	construcción de naves y plantas industriales, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de naves y plantas industriales	t	\N	\N
154	Edificación de inmuebles comerciales y de servicios, y otras edificaciones no residenciales, excepto la supervisión	aeropuertos (edificios), ampliación, remodelación, mantenimiento o reparación de la obra, aeropuertos (edificios), construcción, agencias de automóviles, ampliación, remodelación, mantenimiento o reparación de la obra, agencias de automóviles, construcción, albercas en interiores, ampliación, remodelación, mantenimiento o reparación de la obra, albercas en interiores, construcción, albergues, ampliación, remodelación, mantenimiento o reparación de la obra, almacenes industriales, ampliación, rem	t	\N	\N
155	Supervisión de edificación de inmuebles comerciales y de servicios, y otras edificaciones no residenciales	construcción de inmuebles comerciales, supervisión, construcción de inmuebles de servicios, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de inmuebles comerciales, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de inmuebles de servicios	t	\N	\N
156	Construcción de obras para el tratamiento, distribución y suministro de agua y drenaje	acueductos, ampliación, remodelación, mantenimiento o reparación de la obra, acueductos, construcción, bocas de acceso (cuerpos de agua), ampliación, remodelación, mantenimiento o reparación de la obra, bocas de acceso (cuerpos de agua), construcción, drenajes pluviales, ampliación, remodelación, mantenimiento o reparación de la obra, drenajes pluviales, construcción, drenajes sanitarios, ampliación, remodelación, mantenimiento o reparación de la obra, drenajes sanitarios, construcción, estacion	t	\N	\N
157	Construcción de sistemas de riego agrícola	canales de irrigación, ampliación, remodelación, mantenimiento o reparación de la obra, canales de irrigación, construcción, estaciones de bombeo para riego agrícola, ampliación, remodelación, mantenimiento o reparación de la obra, estaciones de bombeo para riego agrícola, construcción, sistemas de riego, ampliación, remodelación, mantenimiento o reparación de la obra, sistemas de riego, construcción, trabajos especializados que requieren habilidades y equipo específicos para la construcción de 	t	\N	\N
158	Supervisión de construcción de obras para el tratamiento, distribución y suministro de agua, drenaje y riego	construcción de obras para drenaje, supervisión, construcción de obras para el tratamiento, distribución y suministro de agua, supervisión, construcción de sistemas de riego agrícola, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras para drenaje, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras para el tratamiento, distri	t	\N	\N
159	Construcción de sistemas de distribución de petróleo y gas	centrales de gas, ampliación, remodelación, mantenimiento o reparación de la obra, centrales de gas, construcción, ductos para distribución de gas, ampliación, remodelación, mantenimiento o reparación de la obra, ductos para distribución de gas, construcción, ductos para distribución de petróleo, ampliación, remodelación, mantenimiento o reparación de la obra, ductos para distribución de petróleo, construcción, estaciones de bombeo de gas, ampliación, remodelación, mantenimiento o reparación de 	t	\N	\N
160	Construcción de plantas de refinería y petroquímica	plantas de procesamiento de gas natural, ampliación, remodelación, mantenimiento o reparación de la obra, plantas de procesamiento de gas natural, construcción, plantas petroquímicas, ampliación, remodelación, mantenimiento o reparación de la obra, plantas petroquímicas, construcción, refinerías de petróleo, ampliación, remodelación, mantenimiento o reparación de la obra, refinerías de petróleo, construcción, trabajos especializados que requieren habilidades y equipo específicos para la construc	t	\N	\N
161	Supervisión de construcción de obras para petróleo y gas	construcción de obras para petróleo y gas, supervisión, construcción de obras relacionadas con los sistemas de distribución de petróleo y gas, supervisión, construcción de plantas de refinería y petroquímica, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras para petróleo y gas, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de o	t	\N	\N
162	Construcción de obras de generación y conducción de energía eléctrica	cables aéreos para transmisión de energía eléctrica, tendido, cables para transmisión de energía eléctrica, mantenimiento o reparación de la obra, cables para transmisión de energía eléctrica, tendido, cables subterráneos para transmisión de energía eléctrica, tendido, centrales eléctricas, ampliación, remodelación, mantenimiento o reparación de la obra, centrales eléctricas, construcción, estaciones y subestaciones para la generación y distribución de energía eléctrica, ampliación, remodelación	t	\N	\N
163	Construcción de obras para telecomunicaciones	antenas para telecomunicaciones, instalación (excepto por compañías de telecomunicaciones), antenas para telecomunicaciones, mantenimiento o reparación de la obra (excepto por compañías de telecomunicaciones), cables aéreos para telecomunicaciones, tendido, cables para telecomunicaciones, mantenimiento o reparación de la obra, cables subterráneos para telecomunicaciones, tendido, centrales telefónicas, construcción, centrales telefónicas, mantenimiento o reparación de la obra, estaciones de rece	t	\N	\N
164	Supervisión de construcción de obras de generación y conducción de energía eléctrica y de obras para telecomunicaciones	construcción de obras de generación y conducción de energía eléctrica, supervisión, construcción de obras para telecomunicaciones, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras de generación y conducción de energía eléctrica, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras para telecomunicaciones	t	\N	\N
165	División de terrenos	deslinde y marcación de terrenos para la construcción, fraccionamiento de terrenos, subdivisión de terrenos, subdivisión de terrenos (excepto cementerios)	t	\N	\N
166	Construcción de obras de urbanización	alumbrado público (urbanización por fraccionadores), construcción, banquetas (urbanización por fraccionadores), construcción, calles o avenidas (urbanización por fraccionadores), construcción, redes de agua potable (urbanización por fraccionadores), construcción de, redes de alcantarillado (urbanización por fraccionadores), construcción, redes de distribución de gas para edificaciones residenciales (urbanización por fraccionadores), construcción, trabajos especializados que requieren habilidades	t	\N	\N
969	Servicios de emergencia comunitarios prestados por el sector público	refugios alpinos del sector público, servicios de, refugios temporales del sector público para personas afectadas por catástrofes, servicios de, refugios temporales del sector público para personas afectadas por siniestros, servicios de	t	\N	\N
167	Supervisión de división de terrenos y de construcción de obras de urbanización	construcción de obras de urbanización, supervisión, división de terrenos, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras de urbanización, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la división de terrenos	t	\N	\N
168	Instalación de señalamientos y protecciones en obras viales	defensas metálicas en carreteras, instalación, defensas metálicas en carreteras, mantenimiento o reparación de la obra, estribos para carreteras, instalación, estribos para carreteras, mantenimiento o reparación de la obra, fantasmas para carreteras, instalación, fantasmas para carreteras, mantenimiento o reparación de la obra, guardarrieles para carreteras, instalación, guardarrieles para carreteras, mantenimiento o reparación de la obra, líneas viales en autopistas, mantenimiento o reparación 	t	\N	\N
169	Construcción de carreteras, puentes y similares	accesos para puentes, construcción, accesos para puentes, mantenimiento o reparación, aeropistas, ampliación, remodelación, mantenimiento o reparación de la obra, aeropistas, construcción, aeropistas, nivelación, alquitranado de caminos, autopistas elevadas, ampliación, remodelación, mantenimiento o reparación de la obra, autopistas elevadas, construcción, autopistas, ampliación, remodelación, mantenimiento o reparación de la obra, autopistas, construcción, autopistas, nivelación, avenidas (exce	t	\N	\N
170	Supervisión de construcción de vías de comunicación	construcción de vías de comunicación, supervisión, instalación de señalamientos y protecciones en vías de comunicación, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de vías de comunicación, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la instalación de señalamientos y protecciones en vías de comunicación	t	\N	\N
171	Construcción de presas y represas	bordos, ampliación, remodelación, mantenimiento o reparación de la obra, bordos, construcción, presas, ampliación, remodelación, mantenimiento o reparación de la obra, presas, construcción, relleno de tierra para presas, represas, ampliación, remodelación, mantenimiento o reparación de la obra, represas, construcción, trabajos especializados que requieren habilidades y equipo específicos para la construcción de presas, represas y bordos	t	\N	\N
172	Construcción de obras marítimas, fluviales y subacuáticas	ataguías, construcción, ataguías, mantenimiento o reparación de la obra, atracaderos, ampliación, remodelación, mantenimiento o reparación de la obra, atracaderos, construcción, canales de drenaje, ampliación, remodelación, mantenimiento o reparación de la obra, canales de drenaje, construcción, canales, ampliación, mantenimiento o reparación de la obra, canales, construcción, construcciones subacuáticas, construcciones subacuáticas, ampliación, remodelación, mantenimiento o reparación de la obr	t	\N	\N
173	Construcción de obras para transporte eléctrico y ferroviario	balasto en vías férreas, instalación, balasto en vías férreas, mantenimiento, instalaciones eléctricas en vías férreas, colocación, instalaciones eléctricas en vías férreas, mantenimiento o reparación de la obra, instalaciones para teleféricos, ampliación, remodelación, mantenimiento o reparación de la obra, instalaciones para teleféricos, colocación, líneas ferroviarias, construcción, líneas ferroviarias, mantenimiento o reparación de la obra, líneas para tranvías, construcción, líneas para tra	t	\N	\N
174	Supervisión de construcción de otras obras de ingeniería civil	construcción de obras marítimas, fluviales y subacuáticas, supervisión, construcción de obras para transporte eléctrico y ferroviario, supervisión, construcción de presas y represas, supervisión, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras marítimas, fluviales y subacuáticas, supervisión del manejo de recursos materiales, cumplimiento de costos y especificaciones técnicas durante la construcción de obras para 	t	\N	\N
175	Otras construcciones de ingeniería civil	albercas en exteriores, ampliación, remodelación, mantenimiento o reparación de la obra, albercas en exteriores, construcción, bases para monumentos (estatuas, bustos, fuentes), ampliación, remodelación, mantenimiento o reparación de la obra, bases para monumentos (estatuas, bustos, fuentes), construcción, campos atléticos (excepto estadios), ampliación, remodelación, mantenimiento o reparación de la obra, campos atléticos (excepto estadios), construcción, campos de golf, ampliación, remodelació	t	\N	\N
176	Trabajos de cimentaciones	bases de concreto, construcción, castillos, instalación, cimentaciones de concreto, construcción, cimentaciones de edificios, construcción, cimentaciones de edificios, construcción con concreto vaciado, cimentaciones de madera, construcción, cimentaciones especializadas, construcción, cimentaciones, ampliación, mantenimiento o reparación de la obra, cimentaciones, construcción, cimientos de madera permanentes, instalación, losas de cimentación, hincado, pilotes en tierra, hincado	t	\N	\N
177	Montaje de estructuras de concreto prefabricadas	balcones de concreto precolado, montaje en el sitio de la obra, desmantelamiento de formas de concreto colado, escaleras de concreto prevaciado, montaje en el sitio de la obra, estructuras de concreto prefabricadas, montaje en el sitio de la obra, formas de concreto colado, montaje en el sitio de la obra, losas de concreto prevaciado, montaje en el sitio de la obra, paneles de concreto prevaciado, montaje en el sitio de la obra, paredes de cortina de concreto precolado, montaje en el sitio de la	t	\N	\N
178	Montaje de estructuras de acero prefabricadas	acero de reforzamiento, montaje en el sitio de la obra, acero estructural, montaje en el sitio de la obra, balcones de acero, montaje en el sitio de la obra, barras de acero, montaje en el sitio de la obra, barras de reforzamiento de acero, montaje en el sitio de la obra, columnas de acero, montaje en el sitio de la obra, escaleras de acero, montaje en el sitio de la obra, estructuras de acero, montaje en el sitio de la obra, mallas de reforzamiento de acero, montaje en el sitio de la obra, pare	t	\N	\N
179	Trabajos de albañilería	aplanados a base de mortero (trabajos de albañilería), aplicación, bardas de bloques o ladrillos (trabajos de albañilería), levantamiento, bloques de cemento (trabajos de albañilería), instalación, bloques de ceniza (trabajos de albañilería), instalación, bloques de concreto (trabajos de albañilería), instalación, castillos (trabajos de albañilería), instalación, chimeneas de bloque residenciales (trabajos de albañilería), instalación, chimeneas de ladrillo residenciales (trabajos de albañilería	t	\N	\N
462	Fabricación de motocicletas	bastidores para motocicletas, fabricación, bicimotos, fabricación, cuatrimotos, fabricación, motocicletas, fabricación, motonetas, fabricación, sistemas de embrague para motocicletas, fabricación, sistemas de frenos para motocicletas, fabricación, sistemas de suspensión para motocicletas, fabricación, tricimotos, fabricación	t	\N	\N
180	Otros trabajos en exteriores	acero y hierro forjado, instalación de productos decorativos de, bloques de vidrio, instalación, canales pluviales en edificaciones, instalación, canalones sin costura, instalación, componentes de pared prefabricados, instalación, componentes estructurales de madera prefabricados, instalación, contraventanas, instalación, cubiertas de metal, instalación, escalones para techado, instalación, escapes contra incendios, instalación, espejo decorativo para edificios, instalación, espejos para edifici	t	\N	\N
181	Instalaciones eléctricas en construcciones	alumbrado en caminos privados, instalación, alumbrado en estacionamientos privados, instalación, alumbrado público y semáforos, instalación, cables de fibra óptica, instalación en construcciones, cables eléctricos, instalación en construcciones, cables para redes y computadoras, instalación en construcciones, cables para telecomunicaciones, instalación en construcciones, cercas electrónicas, instalación en construcciones, conexión de televisión por cable, instalación en construcciones, controles	t	\N	\N
182	Instalaciones hidrosanitarias y de gas	artículos sanitarios para baño, instalación en construcciones, bombas de cárcamo, instalación en construcciones, calentadores de agua (boilers), instalación en construcciones, calentadores solares de agua, instalación en construcciones, dispositivos para albercas, instalación en construcciones, drenaje, instalación en construcciones, drenaje, mantenimiento o reparación de la obra en construcciones, fregaderos, instalación en construcciones, líneas de gas, instalación en construcciones, medidores	t	\N	\N
183	Instalaciones de sistemas centrales de aire acondicionado y calefacción	aire lavado, instalación de equipo, aire lavado, mantenimiento o reparación de la obra, bombas de calor, instalación, calderas de calefacción, instalación, calefactores, instalación, climas industriales y domésticos, ampliación, remodelación, mantenimiento o reparación de la obra, climas industriales y domésticos, instalación, congeladores comerciales, instalación, ductos de calefacción, instalación, ductos de enfriamiento, instalación, ductos de hoja de metal, instalación, enfriadores de ambien	t	\N	\N
184	Otras instalaciones y equipamiento en construcciones	aislamiento de calderas, instalación en construcciones, aislamiento de ductos, instalación en construcciones, aislamiento de tubería, instalación en construcciones, andadores mecánicos, instalación en construcciones, antenas de tipo doméstico, instalación en construcciones, antenas parabólicas para televisión (TV), instalación en construcciones, bombas de gasolina para estaciones de servicio, instalación, bombas de pozos de agua, instalación, cajeros automáticos, instalación, calderas de energía	t	\N	\N
185	Colocación de muros falsos y aislamiento	acabado de muro seco, instalación, aislamiento acústico, instalación, aislamiento con espuma de estireno, instalación, aislamiento con espuma de uretano, instalación, aislamiento con espuma, instalación, aislamiento con fibra celulosa, instalación, aislamiento con fibra de vidrio, instalación, aislamiento con lana mineral, instalación, aislamiento con panel o tablero rígido, instalación, aislamiento con tableros de poliestireno, instalación, aislamiento contra la vibración, instalación, aislamie	t	\N	\N
186	Trabajos de enyesado, empastado y tiroleado	aplanado de paredes, empastado a base de grano de mármol, empastado a base de gravilla, enyesado ornamental, enyesado sencillo, texturizado de paredes, tiroleado planchado, tiroleado rústico	t	\N	\N
187	Trabajos de pintura y otros cubrimientos de paredes	aplicación de protector contra la corrosión en paredes, cubrimiento de paredes con materiales ornamentales (excepto papel tapiz y telas), mantenimiento o reparación de la obra, cubrimiento de paredes con papel tapiz, mantenimiento o reparación, cubrimiento de paredes con telas, mantenimiento o reparación de la obra, encalado, papel tapiz de paredes, remoción, papel tapiz, instalación, paredes, cubrimiento, pintado de edificaciones, pintores, servicios en construcciones, pintura de interiores y e	t	\N	\N
188	Colocación de pisos flexibles y de madera	acabados de pisos de madera, alfombras, instalación, duela, instalación, hojas de piso flexibles, instalación, linóleo, instalación, loseta vinílica, instalación, losetas, instalación, pisos antifuego, instalación, pisos de acceso, instalación, pisos de asfalto, instalación, pisos de madera dura, instalación, pisos de madera dura, mantenimiento o reparación de la obra, pisos de madera, instalación, pisos de parqué, instalación, pisos de vinil, instalación, pisos flexibles, instalación, pisos lam	t	\N	\N
189	Colocación de pisos cerámicos y azulejos	adoquín (piso), instalación, cerámica (piso), instalación, granito (piso), instalación, loseta (piso), instalación, loseta (piso), pulido, loseta cerámica (piso), instalación, mármol (piso), instalación, mosaico (piso), instalación, piedra (piso), instalación, pizarra (piso), instalación, recubrimientos de cerámica (pisos), instalación, terrazo (piso), instalación, terrazo (piso), pulido	t	\N	\N
190	Realización de trabajos de carpintería en el lugar de la construcción	closets de madera, instalación en el lugar de la construcción, ebanistería en el lugar de la construcción, escaleras de madera, instalación en el lugar de la construcción, estantes de madera, instalación en el lugar de la construcción, gabinetes de madera, instalación en el lugar de la construcción, instalación de productos de carpintería en el lugar de la construcción, molduras de madera, instalación en el lugar de la construcción, paneles de madera para muros, instalación en el lugar de la con	t	\N	\N
191	Otros trabajos de acabados en edificaciones	asientos para espectadores, instalación, cancelería de aluminio, instalación, cortinas metálicas, instalación, cortineros, instalación, desmantelamiento de exhibidores, divisores de metal, instalación, divisores desmontables, instalación, emplomado de paredes de cuartos de rayos X, equipo y mobiliario de laboratorio, instalación, estantería de metal, instalación, exhibidores, instalación, gabinetes de metal, instalación, graderías, instalación, impermeabilización de cimentaciones, impermeabiliza	t	\N	\N
192	Preparación de terrenos para la construcción	barrenado y voladura de edificios, servicios, bulldozers con operador, alquiler, camiones con operador para la construcción, alquiler, compactación de suelos, demolición de edificaciones residenciales y no residenciales, demolición de obras de ingeniería civil, demolición por voladura de edificaciones, desagüe de terrenos para la construcción, desmonte de terrenos para la construcción, desyerbe de terrenos para la construcción, equipo (excepto grúas) con operador para la construcción, alquiler, 	t	\N	\N
193	Otros trabajos especializados para la construcción	adoquinado, instalación, albercas residenciales en exteriores, construcción, andamios, instalación, apuntalamientos, construcción, astas, construcción, buzones de correo, instalación, caminos de entrada comerciales, pavimentación, carteles, instalación, casas móviles, instalación, cercas (excepto electrónicas), instalación, cimbras, instalación, corte de concreto, desmantelamiento de andamios, desmantelamiento de casas móviles, desmantelamiento de elevadores de uso temporal para la construcción,	t	\N	\N
194	Elaboración de alimentos balanceados para animales	alfalfa procesada en paca, elaboración, alimento para animales de laboratorio, elaboración, alimento para ganado a base de harina de alfalfa, elaboración, alimentos balanceados para animales, elaboración, alimentos balanceados para camarones, elaboración, alimentos balanceados para cerdos, elaboración, alimentos balanceados para conejos, elaboración, alimentos balanceados para crecimiento, elaboración, alimentos balanceados para engorda, elaboración, alimentos balanceados para gallos de pelea, e	t	\N	\N
195	Beneficio del arroz	arroz integral, elaboración, arroz, beneficio, arroz, blanqueado, arroz, descascarado, arroz, limpieza, arroz, pulido	t	\N	\N
196	Elaboración de harina de trigo	fulgor (trigo precocido y triturado), elaboración, germen de trigo, elaboración, granillo de trigo, elaboración, harina de trigo, elaboración, salvado de trigo, elaboración, sémola de trigo, elaboración	t	\N	\N
197	Elaboración de harina de maíz	harina de maíz, elaboración, salvado de maíz, elaboración, sémola de maíz, elaboración	t	\N	\N
198	Elaboración de harina de otros productos agrícolas	chiles, molienda, chiles en polvo o quebrados, molienda, harina de alfalfa, elaboración, harina de algodón, elaboración, harina de arroz, elaboración, harina de avena, elaboración, harina de barbasco, elaboración, harina de cebada, elaboración, harina de cempasúchil, elaboración, harina de centeno, elaboración, harina de chiles secos, elaboración, harina de frijol, elaboración, harina de frutas, elaboración, harina de garbanzo, elaboración, harina de habas, elaboración, harina de lentejas, elabo	t	\N	\N
199	Elaboración de malta	extracto de malta, elaboración, malta de arroz, elaboración, malta de cebada, elaboración, malta de centeno, elaboración, malta de maíz, elaboración, malta de trigo, elaboración, malta en grano, elaboración, malta en polvo, elaboración, malta para cerveza, elaboración, malta, elaboración	t	\N	\N
200	Elaboración de féculas y otros almidones y sus derivados	almidón de arroz, elaboración, almidón de maíz, elaboración, almidón de papa, elaboración, almidón de trigo, elaboración, almidón de tubérculos, elaboración, almidón de vegetales, elaboración, dextrina, elaboración, dextrosa, elaboración, fécula de arroz, elaboración, fécula de avena, elaboración, fécula de maíz, elaboración, fécula de papa, elaboración, fécula de trigo, elaboración, féculas, elaboración, fructosa, elaboración, glucosa, elaboración, jarabe o miel de maíz de alta fructosa, elabor	t	\N	\N
201	Elaboración de aceites y grasas vegetales comestibles	aceite comestible de almendra, elaboración, aceite comestible de linaza, elaboración, aceite comestible de nuez, elaboración, aceite comestible en aerosol, elaboración, aceite crudo de semillas oleaginosas, elaboración, aceite crudo de soya, elaboración, aceite crudo vegetal, elaboración, aceite de ajonjolí, elaboración, aceite de cacahuate, elaboración, aceite de canola, elaboración, aceite de cártamo, elaboración, aceite de coco, elaboración, aceite de colza, elaboración, aceite de girasol, el	t	\N	\N
202	Elaboración de cereales para el desayuno	cereales de arroz, elaboración, cereales de avena, elaboración, cereales de hojuelas de maíz, elaboración, cereales de trigo, elaboración, cereales inflados, elaboración, cereales instantáneos, elaboración, cereales mixtos para el desayuno, elaboración, cereales molidos para el desayuno, elaboración, cereales para el desayuno, elaboración, cereales para el lactantes, elaboración, cereales preendulzados, elaboración, cereales procesados, elaboración, cereales rallados, elaboración, cereales recoc	t	\N	\N
203	Elaboración de azúcar de caña	azúcar de caña estándar, elaboración, azúcar de caña granulada, elaboración, azúcar de caña invertida, elaboración, azúcar de caña líquida, elaboración, azúcar de caña morena, elaboración, azúcar de caña para confitería, elaboración, azúcar de caña refinada, elaboración, azúcar de caña sin refinar, elaboración, azúcar de caña, elaboración, azúcar mascabado, elaboración, bagazo de caña, obtención, ingenios azucareros, fábrica, jarabe de azúcar de caña, elaboración, melaza de azúcar de caña, elabo	t	\N	\N
204	Elaboración de otros azúcares	azúcar de arce, refinación, azúcar de remolacha granulada, elaboración, azúcar de remolacha invertida, elaboración, azúcar de remolacha no refinada, elaboración, azúcar de remolacha para confitería, elaboración, azúcar de remolacha refinada, elaboración, azúcar de remolacha, elaboración, edulcorantes de agave, elaboración, edulcorantes de estevia, fabricación, edulcorantes de origen natural, elaboración, jarabe de remolacha, elaboración, melaza de remolacha, elaboración, miel o jarabe de agave, 	t	\N	\N
205	Elaboración de dulces, chicles y productos de confitería que no sean de chocolate	ates, elaboración, barras de galleta cubiertas sin chocolate, elaboración, barras de granola, elaboración, base para la goma de mascar, elaboración, bombones, elaboración, cajeta de leche de cabra, elaboración, cajeta de leche de vaca, elaboración, cajetas, elaboración, caramelos macizos, elaboración, chicles, elaboración, chiclosos, elaboración, chongos zamoranos, elaboración, crema de malvavisco, elaboración, dulces a base de leche, elaboración, dulces cubiertos de chocolate, elaboración a par	t	\N	\N
206	Elaboración de chocolate y productos de chocolate	barras de chocolate, elaboración, cacao para la elaboración de chocolates, procesamiento, cacao, beneficio, chocolate artificial, elaboración, chocolate de mesa, elaboración, chocolate en polvo, elaboración, chocolate instantáneo, elaboración, chocolate para repostería, elaboración, chocolate sintético, elaboración, chocolate sólido, elaboración, chocolates y productos de chocolate, elaboración, chocolates, elaboración, cocoa en polvo, elaboración, cocoa instantánea, elaboración, cubiertas de ch	t	\N	\N
207	Congelación de frutas y verduras	aguacates congelados, elaboración, apio congelado, elaboración, aros de cebolla congelados, elaboración, brócolis congelados, elaboración, calabacitas congeladas, elaboración, chabacanos congelados, elaboración, champiñones congelados, elaboración, chayotes congelados, elaboración, chícharos congelados, elaboración, chiles congelados, elaboración, coliflores congeladas, elaboración, concentrados de fruta congelados, elaboración, concentrados de verduras y vegetales congelados, elaboración, duraz	t	\N	\N
208	Congelación de guisos y otros alimentos preparados	alimentos preparados congelados, elaboración, burritos congelados, elaboración, carne preparada para hamburguesas, elaboración, enchiladas congeladas, elaboración, guisos congelados a base de carnes, elaboración, guisos congelados a base de verduras y legumbres, elaboración, guisos congelados, elaboración, guisos dietéticos congelados, elaboración, nuggets congelados, elaboración, pizzas congeladas, elaboración, quesadillas congeladas, elaboración, salsas congeladas, elaboración, sopas congelada	t	\N	\N
463	Fabricación de bicicletas y triciclos	bicicletas para niños, fabricación, bicicletas, fabricación, cuadriciclos, fabricación, triciclos de carga, fabricación, triciclos para niños, fabricación, triciclos, fabricación	t	\N	\N
1066	Sanitarios públicos y bolerías	bolerías, servicios de, calzado, limpieza, calzado, lustrado, sanitarios públicos, servicios de	t	\N	\N
209	Deshidratación de frutas y verduras	aceitunas deshidratadas, elaboración, ajos deshidratados, elaboración, almendras deshidratadas, elaboración, brócolis deshidratados, elaboración, camotes deshidratados, elaboración, cáscaras de limón deshidratadas, elaboración, cáscaras de naranja deshidratadas, elaboración, cebollas deshidratadas, elaboración, cerezas deshidratadas, elaboración, chabacanos deshidratados, elaboración, chiles secos o deshidratados, elaboración, ciruelas deshidratadas, elaboración, cocos deshidratados, elaboración	t	\N	\N
210	Conservación de frutas y verduras por procesos distintos a la congelación y la deshidratación	aceitunas en salmuera, elaboración, aceitunas enlatadas, elaboración, alcachofas enlatadas, elaboración, cebollas en salmuera, elaboración, cebollas enlatadas, elaboración, champiñones en salmuera, elaboración, champiñones enlatados, elaboración, chícharos enlatados, elaboración, chiles en escabeche, elaboración, cócteles de frutas enlatados, elaboración, coliflores en salmuera, elaboración, coliflores enlatadas, elaboración, duraznos en almíbar, elaboración, duraznos enlatados, elaboración, esp	t	\N	\N
211	Conservación de guisos y otros alimentos preparados por procesos distintos a la congelación	adobos, elaboración, alimentos para bebé colados y picados a base de carnes y verduras, elaboración, alimentos para bebé colados y picados a base de frutas, elaboración, alimentos para bebé colados y picados a base de verduras, elaboración, alimentos para bebé colados y picados, elaboración, alimentos para bebé, elaboración, alimentos preparados deshidratados, elaboración, alimentos preparados enlatados, elaboración, caldillos y caldos condensados a base de verduras y carnes, elaboración, concen	t	\N	\N
212	Elaboración de leche líquida	leche líquida con sabor a chocolate, elaboración, leche líquida de soya, elaboración, leche líquida desodorizada, elaboración, leche líquida descremada, elaboración, leche líquida deslactosada, elaboración, leche líquida dietética, elaboración, leche líquida entera, elaboración, leche líquida homogeneizada, elaboración, leche líquida light, elaboración, leche líquida para lactantes, elaboración, leche líquida pasteurizada, elaboración, leche líquida reconstituida, elaboración, leche líquida sabo	t	\N	\N
213	Elaboración de leche en polvo, condensada y evaporada	leche condensada, elaboración, leche deshidratada, elaboración, leche en polvo de soya, elaboración, leche en polvo descremada, elaboración, leche en polvo dietética, elaboración, leche en polvo entera, elaboración, leche en polvo para lactantes, elaboración, leche en polvo semidescremada, elaboración, leche en polvo, elaboración, leche evaporada, elaboración, mezclas de leche en polvo, elaboración	t	\N	\N
214	Elaboración de derivados y fermentos lácteos	bebidas a base de lactobacilos, elaboración, caseína, elaboración, crema ácida, elaboración, crema batida, elaboración, crema comestible de imitación, elaboración, crema comestible de leche, elaboración, crema deshidratada o pulverizada, elaboración, crema dulce, elaboración, cuajada de queso, elaboración, derivados lácteos, elaboración, dips a base de queso, elaboración, fermentos lácteos, elaboración, lactosa, fabricación, leche búlgara, elaboración, mantequilla reconstituida, elaboración, man	t	\N	\N
215	Elaboración de helados y paletas	bolis, elaboración, congeladas de frutas, elaboración, helados, elaboración, mixtura o base para helados, elaboración, natillas congeladas, elaboración, nevería, fábrica, nieves, elaboración, paletas a base de agua, elaboración, paletas a base de leche, elaboración, paletas a base de yogur, elaboración, paletas de hielo, elaboración, paletería, fábrica, raspados o granizados, elaboración, sorbetes, elaboración, tofu (postre congelado), elaboración	t	\N	\N
216	Matanza de ganado, aves y otros animales comestibles	animales comestibles, matanza, asnos, matanza, aves, matanza, avestruces, matanza, borregos, matanza, bovinos, matanza, caballos, matanza, cabritos, matanza, caprinos, matanza, cerdos, matanza, chivos, matanza, codornices, matanza, conejos, matanza, corderos, matanza, cueros y pieles en bruto, ganado asnal, matanza, ganado bovino, matanza, ganado caprino, matanza, ganado equino, matanza, ganado mular, matanza, ganado ovino, matanza, ganado porcino, matanza, ganado, matanza, gansos, matanza, guaj	t	\N	\N
217	Corte y empacado de carne de ganado, aves y otros animales comestibles	carne comestible, selección, corte, deshuesado, congelado o empacado, carne de asno, selección, corte, deshuesado, congelado o empacado, carne de aves, selección, corte, deshuesado, congelado o empacado, carne de avestruz, selección, corte, deshuesado, congelado o empacado, carne de borrego, selección, corte, deshuesado, congelado o empacado, carne de bovino, selección, corte, deshuesado, congelado o empacado, carne de caballo, selección, corte, deshuesado, congelado o empacado, carne de cabrito	t	\N	\N
218	Elaboración de embutidos y otras conservas de carne de ganado, aves y otros animales comestibles	carnes adobadas, elaboración, carnes ahumadas, elaboración, carnes condimentadas, elaboración, carnes en conserva, elaboración, carnes encurtidas, elaboración, carnes enlatadas, elaboración, carnes frías, elaboración, carnes marinadas, elaboración, carnes saladas, elaboración, carnes secas, elaboración, chorizo, elaboración, chuletas ahumadas, elaboración, embutidoras de carne, fábricas, embutidos, elaboración, extractos de carne, elaboración, harina de carnes, elaboración, jamones, elaboración,	t	\N	\N
219	Elaboración de manteca y otras grasas animales comestibles	aceites comestibles de origen animal, elaboración, aceites comestibles de origen animal, refinación, cuero sancochado para chicharrón, elaboración, grasas comestibles de origen animal, elaboración, manteca de cerdo, elaboración, manteca de res, elaboración	t	\N	\N
220	Preparación y envasado de pescados y mariscos	aceite crudo de hígado de bacalao, elaboración, aceite de pescado, elaboración, aletas de tiburón, preparación y envasado, algas marinas, preparación y envasado, almejas, preparación y envasado, atún, preparación y envasado, bacalao, secado y salado, barcos fabrica de pescados y mariscos, caldos a base de pescados y mariscos, elaboración, camarones, preparación y envasado, cangrejos, preparación y envasado, caracoles, preparación y envasado, caviar, preparación y envasado, charales, secado y sal	t	\N	\N
221	Panificación industrial	buñuelos, panificación industrial, donas, panificación industrial, galletas horneadas, panificación industrial, pan blanco de trigo, panificación industrial, pan congelado, panificación industrial, pan de caja, panificación industrial, pan de centeno, panificación industrial, pan de dulce, panificación industrial, pan de sal, panificación industrial, pan de salvado, panificación industrial, pan empacado, panificación industrial, pan integral de trigo, panificación industrial, pan, panificación i	t	\N	\N
464	Fabricación de otro equipo de transporte	autos de carrera, fabricación, carros de golf para pasajeros y set de golf, fabricación, carros para expender productos, fabricación, go-karts, fabricación, tanques militares, fabricación, vehículos de tracción animal, fabricación, vehículos eléctricos roll-car, fabricación	t	\N	\N
222	Panificación tradicional	baguettes, panificación tradicional, birotes, panificación tradicional, bolillos, panificación tradicional, buñuelos, panificación tradicional, donas, panificación tradicional, empanadas, panificación tradicional, pan blanco de trigo, panificación tradicional, pan de centeno, panificación tradicional, pan de dulce, panificación tradicional, pan de sal, panificación tradicional, pan de salvado, panificación tradicional, pan integral de trigo, panificación tradicional, pan, panificación tradiciona	t	\N	\N
223	Elaboración de tortillas de harina de trigo de forma tradicional	tortillas de harina de trigo, tortillería tradicional	t	\N	\N
224	Elaboración de galletas y pastas para sopa	barquillos para helado, elaboración, bases para pay no horneadas, elaboración, conos para helado, elaboración, galletas dulces, elaboración, galletas saladas, elaboración, galletas, elaboración, harina premezclada para crepas, elaboración, harina premezclada para donas, elaboración, harina premezclada para galletas, elaboración, harina premezclada para hot cakes, elaboración, harina premezclada para pasteles, elaboración, harina premezclada para repostería, elaboración, obleas (excepto de golosi	t	\N	\N
225	Elaboración de tortillas de maíz y molienda de nixtamal	maíz húmedo, molienda, molinos de nixtamal, nixtamal, molienda, tortillas de maíz, elaboración, tortillerías de tortillas de maíz, fábrica	t	\N	\N
226	Elaboración de botanas	almendras fritas y saladas (botana), elaboración, botanas de harina para freír, elaboración, botanas de harina, elaboración, botanas de maíz, elaboración, botanas de papa, elaboración, botanas de pistache, elaboración, botanas fritas, elaboración, botanas tostadas, elaboración, botanas, elaboración, cacahuates enchilados (botana), elaboración, cacahuates fritos (botana), elaboración, cacahuates japoneses (botana), elaboración, chicharrones de cerdo (botana), elaboración, chicharrones de harina (	t	\N	\N
227	Beneficio del café	café, beneficio, café, despulpado, café, lavado, café, limpieza, café, morteado, café, secado	t	\N	\N
228	Elaboración de café tostado y molido destinado a unidades que lo comercializan	café en grano descafeinado, elaboración, café tostado en grano, elaboración, café tostado molido, elaboración, café, molienda	t	\N	\N
229	Elaboración de café instantáneo	café descafeinado, elaboración, café instantáneo descafeinado, elaboración, café instantáneo, elaboración, café sintético, elaboración, café soluble, elaboración, concentrados de café, elaboración, extractos y esencias de café, elaboración, jarabe y saborizantes de café, elaboración, mezclas de café, elaboración, polvos para café tipo capuchino, elaboración, polvos para café tipo moka, elaboración, polvos para café tipo vienés, elaboración, saborizantes de café, elaboración, sustitutos de café, 	t	\N	\N
230	Preparación y envasado de té	concentrados de té, elaboración, esencias de té, elaboración, extracto de té, elaboración, mezclas de té, elaboración, té instantáneo, elaboración, té sintético, elaboración, té, preparación y envasado	t	\N	\N
231	Elaboración de concentrados, polvos, jarabes y esencias de sabor para bebidas	colorantes naturales para alimentos, elaboración, concentrados para bebidas, elaboración, esencias de sabor para bebidas, elaboración, esencias de sabor para gelatinas, elaboración, esencias de sabor para refrescos, elaboración, extracto de jamaica para bebidas, elaboración, extracto de tamarindo para bebidas, elaboración, extractos para bebidas, elaboración, jarabes para preparar bebidas, elaboración, jarabes saborizantes para bebidas, elaboración, polvos para preparar bebidas, elaboración, sab	t	\N	\N
232	Elaboración de condimentos y aderezos	ablandadores de carne, elaboración, achiote (condimento), elaboración, aderezos de soya, elaboración, aderezos, elaboración, ajos en polvo, elaboración, anís de estrella (condimento), elaboración, apio en polvo, elaboración, azafrán, elaboración, canela (condimento), elaboración, cebollas en polvo, elaboración, cilantro en polvo, elaboración, clavo (especias), elaboración, comino seco y en polvo, elaboración, condimentos, elaboración, especias y condimentos secos, elaboración, extracto de vainil	t	\N	\N
233	Elaboración de gelatinas y otros postres en polvo	budines en polvo, elaboración, flanes en polvo, elaboración, gelatinas comestibles en polvo, elaboración, grenetina comestible, elaboración, natillas en polvo, elaboración, postres en polvo, elaboración	t	\N	\N
234	Elaboración de levadura	levadura, elaboración	t	\N	\N
235	Elaboración de alimentos frescos para consumo inmediato	alimentos frescos para consumo inmediato, elaboración para su distribución, budines preparados, elaboración para su distribución, ensaladas frescas para consumo inmediato, elaboración para su distribución, flanes preparados, elaboración para su distribución, gelatinas comestibles preparadas, elaboración para su distribución, hamburguesas, elaboración para su distribución, hot dogs, elaboración para su distribución, pizzas frescas, elaboración para su distribución, sándwiches, elaboración para su	t	\N	\N
236	Elaboración de otros alimentos procesados y envasados	aguacate fresco, cortado o machacado, elaboración, azúcar compactada, elaboración, azúcar glas, elaboración, coco rallado, elaboración, crema chantillí, elaboración, frutas peladas y cortadas, elaboración, glaseados preparados para repostería, elaboración, grageas para repostería, elaboración, huevo en polvo, elaboración, huevo líquido, elaboración, huevo procesado, elaboración, jarabe de sorgo, fabricación, jarabe para hot cakes excepto maple, elaboración, merengue para repostería, elaboración,	t	\N	\N
237	Elaboración de refrescos y otras bebidas no alcohólicas	agua con sabor, elaboración, agua gasificada, elaboración, agua mineralizada, elaboración, agua quinada, elaboración, bebidas carbonatadas, elaboración, bebidas con sabor a frutas, elaboración, bebidas energéticas (energizantes), elaboración, bebidas gasificadas, elaboración, bebidas hidratantes, elaboración, bebidas no carbonatadas, elaboración, café helado preparado y envasado, elaboración, mezclas de bebidas sin grado alcohólico, elaboración, refrescos de envase no retornable, elaboración, re	t	\N	\N
238	Purificación y embotellado de agua	agua purificada, elaboración, agua sin sabor, purificación y embotellado, purificación de agua donde se llena directamente el garrafón a los clientes	t	\N	\N
239	Elaboración de hielo	cubos de hielo potable purificado, elaboración, hielo potable purificado, elaboración	t	\N	\N
240	Elaboración de cerveza	cerveza amarga, elaboración, cerveza clara, elaboración, cerveza de barril, elaboración, cerveza de grano, elaboración, cerveza de malta, elaboración, cerveza embotellada, elaboración, cerveza en lata, elaboración, cerveza lager, fabricación, cerveza obscura, elaboración, cerveza sin alcohol, elaboración, cerveza, elaboración, licor de malta de cerveza, elaboración	t	\N	\N
465	Fabricación de cocinas integrales y muebles modulares de baño	cocinas integrales, fabricación, cocinas modulares, fabricación, cubiertas para cocinetas, fabricación, gabinetes de cocina integral, fabricación, muebles integrales de baño, fabricación, muebles modulares de baño, fabricación	t	\N	\N
241	Elaboración de bebidas alcohólicas a base de uva	aguardiente de uva, elaboración, bebidas destiladas a base de uva, elaboración, bebidas fermentadas a base de uva, elaboración, brandy, elaboración, champaña (champagne), elaboración, coñac (cognac), elaboración, cultivo de uva y elaboración de vino, jerez, elaboración, mezclas que contienen principalmente bebidas alcohólicas a base de uva, elaboración, mezclas de vinos, elaboración, vermut, elaboración, vino blanco, elaboración, vino de consagrar, elaboración, vino rosado, elaboración, vino tin	t	\N	\N
242	Elaboración de pulque	pulque bronco, elaboración, pulque curado, elaboración, pulque de sabores, elaboración, pulque embotellado, elaboración, pulque envasado, elaboración, pulque natural, elaboración, pulque pasteurizado, elaboración, pulque preparado, elaboración, pulque, elaboración	t	\N	\N
243	Elaboración de sidra y otras bebidas fermentadas	mezclas que contienen principalmente bebidas fermentadas, elaboración, perada, elaboración, sake, elaboración, sidra, elaboración, vino de frutas excepto de uva, elaboración	t	\N	\N
244	Elaboración de ron y otras bebidas destiladas de caña	aguardiente de caña, elaboración, mezclas que contienen principalmente bebidas alcohólicas a base de ron y otras bebidas destiladas de caña, elaboración, ron, elaboración	t	\N	\N
245	Obtención de alcohol etílico potable	alcohol etílico potable, obtención, mezclas que contienen principalmente bebidas alcohólicas a base de tequila, elaboración	t	\N	\N
246	Elaboración de tequila	tequila, elaboración, tequila añejo, elaboración, tequila blanco, elaboración, tequila extra añejo, elaboración, tequila joven, elaboración, tequila reposado, elaboración	t	\N	\N
247	Elaboración de mezcal	mezclas que contienen principalmente bebidas alcohólicas a base de mezcal, elaboración, mezcal, elaboración, mezcal añejo, elaboración, mezcal joven, elaboración, mezcal reposado, elaboración, sotol añejo, elaboración, sotol blanco, elaboración, sotol joven, elaboración, sotol reposado, elaboración	t	\N	\N
248	Elaboración de otras bebidas destiladas	aguardientes de agave, elaboración, amareto, elaboración, anís (bebida), elaboración, bases para licores, elaboración, bebidas destiladas excepto a base de uva y caña, elaboración, charanda, elaboración, cocteles a base de tequila, elaboración, ginebra, elaboración, licor de almendras, elaboración, licor de café, elaboración, licor de crema, elaboración, licor de frutas, elaboración, mezclas que contienen principalmente bebidas destiladas, excepto de caña, elaboración, mezclas de licores, elabor	t	\N	\N
249	Beneficio del tabaco	hojas de tabaco, clasificación, procesamiento y envejecimiento de hoja de tabaco, tabaco, beneficio, tabaco, deshidratado, tabaco, desvenado, tabaco, laminado, tabaco, secado	t	\N	\N
250	Elaboración de cigarros	cigarrillos, elaboración, cigarros de tabaco de imitación, elaboración, cigarros, elaboración	t	\N	\N
251	Elaboración de puros y otros productos de tabaco	puros, elaboración, tabaco en polvo, elaboración, tabaco para mascar, elaboración, tabaco para pipa, elaboración, tabaco rapé, elaboración, tabaco reconstituido, elaboración	t	\N	\N
252	Preparación e hilado de fibras duras naturales	artículos decorativos de fibras duras naturales, fabricación a partir de fibra preparada o comprada, bolsos de mano de fibras duras naturales, tejido a partir de fibra preparada o comprada, canastos de fibras duras naturales, tejido a partir de fibra preparada o comprada, canastos de palma, tejido a partir de fibra preparada o comprada, cáñamo, hilado, cerdas textiles, preparación, cestos de fibras duras naturales, tejido a partir de fibra preparada o comprada, cestos de palma, tejido a partir d	t	\N	\N
253	Preparación e hilado de fibras blandas naturales	algodón, hilado, algodón, preparación, estambres de fibras naturales, fabricación, estambres de fibras sintéticas, fabricación, estambres de lana, fabricación, estambres, fabricación, fibra de amianto, hilado, fibras blandas de origen animal, desengrasado, fibras blandas naturales, blanqueado, fibras blandas naturales, cardado, fibras blandas naturales, devanado, fibras blandas naturales, lavado, fibras blandas naturales, peinado, fibras blandas naturales, preparación, fibras de origen químico, 	t	\N	\N
254	Fabricación de hilos para coser y bordar	hilazas, fabricación, hilo de fibra de vidrio, fabricación, hilos de algodón, fabricación, hilos de amianto (asbesto), fabricación, hilos de angora, fabricación, hilos de elastómeros, fabricación, hilos de fibra animal, fabricación, hilos de fibra natural, fabricación, hilos de hule, fabricación, hilos de lana, fabricación, hilos de lino, fabricación, hilos de llama, fabricación, hilos de mezclas de fibra, fabricación, hilos de nailon, fabricación, hilos de poliéster, fabricación, hilos de propi	t	\N	\N
255	Fabricación de telas anchas de tejido de trama	blancos, confección integrada con la fabricación de tela, bombasí, fabricación, bramante, fabricación, brocado, fabricación, casimires, fabricación, chifón, fabricación, cobertores, confección integrada con la fabricación de tela, cobijas, confección integrada con la fabricación de tela, colchas, confección integrada con la fabricación de tela, crepé (tela), fabricación, crinolina (tela), fabricación, dacrón, fabricación, dril, fabricación, dubetina, fabricación, edredones, confección integrada 	t	\N	\N
256	Fabricación de telas angostas de tejido de trama y pasamanería	bies (pasamanería), fabricación, borlas (pasamanería), fabricación, chaquiras, fabricación, cintas decorativas, fabricación, cintas elásticas tejidas, fabricación, cintas textiles para calzado excepto agujetas, fabricación, cintas textiles, fabricación, encajes (pasamanería), fabricación, etiquetas de tela, fabricación, flecos (pasamanería), fabricación, galones (pasamanería), fabricación, jergas (telas angostas), fabricación, lentejuelas, fabricación, listones (pasamanería), fabricación, pasama	t	\N	\N
257	Fabricación de telas no tejidas (comprimidas)	entretelas, fabricación, fieltro (tela), fabricación, guatas, fabricación, laminados textiles, fabricación, telas absorbentes no tejidas, fabricación, telas comprimidas, fabricación, telas no tejidas (comprimidas) de uso industrial, fabricación, telas no tejidas (comprimidas) de uso quirúrgico, fabricación, telas no tejidas (comprimidas) de uso sanitario, fabricación, telas no tejidas integrada con la confección de productos textiles, fabricación	t	\N	\N
258	Fabricación de telas de tejido de punto	blancos, confección integrada con la fabricación de la tela de tejido de punto, carpetas, tejido de punto, colchas, confección integrada con la fabricación de tela de tejido de punto, colchas, tejido de punto, cortinas, confección integrada con la fabricación de la tela de tejido de punto, manteles, confección integrada con la fabricación de tela de tejido de punto, manteles, tejido de punto, sábanas, confección integrada con la fabricación de la tela de tejido de punto, telas angostas de tejido	t	\N	\N
259	Acabado de productos textiles	acabado antiarrugas de telas a partir de telas compradas, acabado antiarrugas de telas propiedad de terceros, acabado de fibras textiles a partir de fibra comprada, acabado de fibras textiles propiedad de terceros, acabado de hilados a partir de hilo comprado, acabado de hilados propiedad de terceros, acabado de hilos a partir de hilos comprados, acabado de hilos propiedad de terceros, acabado de telas a partir de telas compradas, acabado de telas propiedad de terceros, acabado de textiles propi	t	\N	\N
260	Fabricación de telas recubiertas	ahulado de telas a partir de tela comprada, ahulado de telas propiedad de terceros, aluminizado de telas a partir de tela comprada, aluminizado de telas propiedad de terceros, bañado de telas a partir de tela comprada, bañado de telas propiedad de terceros, barnizado de telas a partir de tela comprada, barnizado de telas propiedad de terceros, encerado de telas a partir de tela comprada, encerado de telas propiedad de terceros, engomado de telas a partir de tela comprada, engomado de telas propi	t	\N	\N
261	Fabricación de alfombras y tapetes	alfombras, anudado a partir de hilo comprado, alfombras, confección a partir de tela comprada, alfombras, tejido a partir de hilo comprado, césped sintético o artificial, fabricación, esteras, anudado a partir de hilo comprado, esteras, confección a partir de tela comprada, esteras, tejido a partir de hilo comprado, tapetes, anudado a partir de hilo comprado, tapetes, confección a partir de tela comprada, tapetes, tejido a partir de hilo comprado	t	\N	\N
262	Confección de cortinas, blancos y similares	adornos de materiales textiles para cortinas, confección a partir de tela comprada, almohadas, confección a partir de tela comprada, almohadones, confección a partir de tela comprada, blancos, confección a partir de tela comprada, cenefas, confección a partir de tela comprada, cobertores, confección a partir de tela comprada, cobijas, confección a partir de tela comprada, cojines, confección a partir de tela comprada, colchas, confección a partir de tela comprada, colchonetas, confección a parti	t	\N	\N
263	Confección de costales	bolsas para empaque y embalaje, confección a partir de materiales textiles comprados, bolsas para empaque y embalaje, confección a partir de tela comprada, costales de fibras de origen químico, tejido a partir de hilo comprado, costales de lona, confección a partir de tela comprada, costales de manta, confección a partir de tela comprada, costales de polipropileno, confección a partir de tela comprada, costales de polipropileno, tejido a partir de hilo comprado, costales de rafia, confección a p	t	\N	\N
264	Confección de productos de textiles recubiertos y de materiales sucedáneos	alforjas de lona, confección, bolsas para dormir, confección, bolsas para lavandería y tintorería, confección, carpas, confección, cubiertas de lona, confección, cubiertas para automóviles, camiones y camionetas, confección, cubiertas para muebles, confección, lonas para camión, confección, lonas para sombra, confección, lonas vinílicas, confección, paracaídas, confección, parasoles, confección, tiendas de campaña, confección, toldos de lona excepto de automóvil, confección, toldos de materiales	t	\N	\N
265	Confección, bordado y deshilado de productos textiles	bordado con chaquira y lentejuela sobre prendas de vestir, carpetas, bordado, carpetas, confección, bordado y deshilado, carpetas, deshilado, gorras, bordado, manteles, bordado, manteles, bordado y deshilado, manteles, confección, bordado y deshilado, manteles, deshilado, pañuelos, bordado, pañuelos, bordado y deshilado, pañuelos, confección, bordados y deshilados, pañuelos, deshilado, playeras, bordado, prendas de vestir, bordado, prendas de vestir, bordado y deshilado, prendas de vestir, deshi	t	\N	\N
266	Fabricación de redes y otros productos de cordelería	cables de algodón, fabricación, cables de materiales textiles, fabricación, cables de nailon, fabricación, cables de poliéster, fabricación, cables de polipropileno, fabricación, cordelería reforzada, fabricación, cordelería trenzada, fabricación, cordelería, fabricación, cordeles de materiales textiles, fabricación, cordeles y cabos de sisal o demás fibras textiles del género agave a partir de hilo comprado, fabricación, cordones de nailon, fabricación, cordones de polietileno, fabricación, cor	t	\N	\N
267	Fabricación de borras y estopas	borras, fabricación a partir de textiles reciclados, estopas, fabricación a partir de textiles reciclados	t	\N	\N
268	Fabricación de banderas y otros productos textiles no clasificados en otra parte	adornos para muebles de materiales textiles, fabricación, banderas, fabricación, banderines, fabricación, cintas textiles para sellar puertas y ventanas, fabricación, encajes termoformados, fabricación, escudos, fabricación, estandartes, fabricación, filtros textiles, fabricación, forros para ataúd, fabricación, forros para equipaje, fabricación, gallardetes, fabricación, insignias, fabricación, mangueras textiles, fabricación, pañales de tela, confección, paños para limpieza de tela comprada, f	t	\N	\N
269	Fabricación de calcetines y medias de tejido de punto	calcetas de tejido de punto, fabricación, calcetines de tejido de punto con suela antideslizante, fabricación, calcetines de tejido de punto, fabricación, calentadores de tejido de punto (prendas de vestir), fabricación, leotardos de tejido de punto, fabricación, mallas para vestir de tejido de punto, fabricación, mallones tejido de punto, fabricación, medias de tejido de punto, fabricación, pantimedias de tejido de punto, fabricación, tines de tejido de punto, fabricación, tobilleras de tejido 	t	\N	\N
270	Fabricación de ropa interior de tejido de punto	batas de baño de tejido de punto, fabricación, brassieres de tejido de punto, fabricación, calzoncillos de tejido de punto, fabricación, calzones de tejido de punto, fabricación, camisetas de tejido de punto, fabricación, camisones de tejido de punto, fabricación, fajas de tejido de punto, fabricación, fondos de tejido de punto, fabricación, mamelucos para dormir de tejido de punto, fabricación, medios fondos de tejido de punto, fabricación, negligés de tejido de punto, fabricación, pantaletas d	t	\N	\N
271	Fabricación de ropa exterior de tejido de punto	abrigos de tejido de punto, fabricación, blusas de tejido de punto, fabricación, bufandas de tejido de punto, fabricación, camisas de tejido de punto, fabricación, capas de tejido de punto, fabricación, chalecos de tejido de punto, fabricación, chalinas de tejido de punto, fabricación, chamarras de tejido de punto, fabricación, chaquetas de tejido de punto, fabricación, conjuntos de vestir de tejido de punto, fabricación, corbatas de tejido de punto, fabricación, cuellos de tejido de punto, fabr	t	\N	\N
272	Confección de prendas de vestir de cuero, piel y materiales sucedáneos	abrigos de materiales sucedáneos del cuero y piel, confección, abrigos de piel, confección, chalecos de cuero, confección, chalecos de gamuza, confección, chalecos de piel, confección, chamarras de cuero, confección, chamarras de gamuza, confección, chamarras de materiales sucedáneos del cuero y piel, confección, chamarras de piel, confección, faldas de cuero, confección, faldas de gamuza, confección, faldas de materiales sucedáneos del cuero y piel, confección, faldas de piel, confección, panta	t	\N	\N
273	Confección en serie de ropa interior y de dormir	batas de baño, confección en serie, batas para dormir, confección en serie, brassieres, confección en serie, calzoncillos, confección en serie, camisones, confección en serie, corpiños, confección en serie, corsés, confección en serie, fajas, confección en serie, fondos, confección en serie, ligueros, confección en serie, pantaletas, confección en serie, pijamas, confección en serie, ropa interior para bebé, confección en serie, ropa interior para caballero, confección en serie, ropa interior pa	t	\N	\N
274	Confección en serie de camisas	camisas, confección en serie, guayaberas, confección en serie	t	\N	\N
275	Confección en serie de uniformes	batas de uniforme, confección en serie, cofias, confección en serie, filipinas, confección en serie, mandiles, confección en serie, overoles de trabajo, confección en serie, ropa de trabajo, confección en serie, uniformes de trabajo, confección en serie, uniformes deportivos, confección en serie, uniformes escolares, confección en serie, uniformes médicos, confección en serie, uniformes militares, confección en serie, uniformes para enfermeras, confección en serie, uniformes para personal de ser	t	\N	\N
276	Confección en serie de disfraces y trajes típicos	disfraces, confección en serie, hábitos religiosos, confección en serie, ropa artística, confección en serie, togas académicas, confección en serie, trajes para torero, confección en serie, trajes regionales, confección en serie, trajes típicos, confección en serie, túnicas, confección en serie, vestuario para teatro, confección en serie	t	\N	\N
277	Confección de prendas de vestir sobre medida	abrigos, confección sobre medida, blusas, confección sobre medida, camisas, confección sobre medida, chalecos, confección sobre medida, chamarras, confección sobre medida, conjuntos de ropa de vestir, confección sobre medida, coordinados de ropa de vestir, confección sobre medida, disfraces, confección sobre medida, faldas, confección sobre medida, gabardinas, confección sobre medida, pantalones, confección sobre medida, prendas de vestir, confección sobre medida, ropa artística, confección sobr	t	\N	\N
278	Confección en serie de otra ropa exterior de materiales textiles	abrigos, confección en serie, baberos para niños, confección en serie, blusas, confección en serie, chalecos, confección en serie, chamarras, confección en serie, conjuntos de vestir, confección en serie, coordinados de prendas de vestir, confección en serie, faldas, confección en serie, gabardinas, confección en serie, impermeables, confección en serie, mamelucos, confección en serie, pantalones, confección en serie, pants, confección en serie, playeras, confección en serie, ropa de etiqueta, c	t	\N	\N
279	Confección de sombreros y gorras	boinas, confección, cachuchas, confección, gorras de licra y poliéster para natación, confección, gorras de materiales textiles, confección, cascos para sombreros, confección, gorras de piel, confección, gorras de tela para natación, confección, gorras de tela, confección, pasamontañas, confección, sombreros de cuero, confección, sombreros de fibras duras, confección, sombreros de fibras plásticas, confección, sombreros de fieltro, confección, sombreros de materiales sucedáneos del cuero y piel,	t	\N	\N
280	Confección de otros accesorios y prendas de vestir no clasificados en otra parte	abanicos, confección, adornos de materiales textiles para sombreros, confección, adornos para accesorios de vestir, confección, bufandas, confección, cinturones de cuero y piel, confección, cinturones de materiales textiles, confección, cinturones, confección, corbatas, confección, cuellos para prendas de vestir excepto de tejido de punto, confección, diademas, confección, guantes de cuero y piel, confección, guantes de materiales textiles, confección, hombreras para prendas de vestir, confecció	t	\N	\N
281	Curtido y acabado de cuero y piel	ante (gamuza), fabricación, charol, fabricación, cuero apergaminado, fabricación, cuero de fantasía, fabricación, cuero de imitación, fabricación, cuero gamuzado, fabricación, cuero grabado, fabricación, cuero metalizado, fabricación, cuero para tapicería, fabricación, cuero regenerado, fabricación, cuero revestido, fabricación, cuero ribeteado, fabricación, cuero, acabado, cuero, adobado, cuero, blanqueado, cuero, curado, cuero, curtido, cuero, depilado, cuero, estampado, cuero, raspado, cuero,	t	\N	\N
282	Fabricación de calzado con corte de piel y cuero	botas con corte de piel y cuero, fabricación, botines con corte de piel y cuero, fabricación, calzado con corte de gamuza, fabricación, calzado con corte de piel y cuero, fabricación, calzado de seguridad con corte de piel y cuero, fabricación, calzado deportivo con corte de piel y cuero, fabricación, calzado para bebé con corte de piel y cuero, fabricación, calzado para caballero con corte de piel y cuero, fabricación, calzado para dama con corte de piel y cuero, fabricación, calzado para niño 	t	\N	\N
283	Fabricación de calzado con corte de tela	alpargatas con corte de tela, fabricación, botas con corte de tela, fabricación, botines con corte de tela, fabricación, calzado con corte de fieltro, fabricación, calzado con corte de lona, fabricación, calzado con corte de tela, fabricación, calzado de seguridad con corte de tela, fabricación, calzado deportivo con corte de tela, fabricación, calzado para bebé con corte de tela, fabricación, calzado para caballero con corte de tela, fabricación, calzado para dama con corte de tela, fabricación	t	\N	\N
284	Fabricación de calzado de plástico	botas de plástico, fabricación, botines de plástico, fabricación, calzado con corte de tela plástica o vinílica, fabricación, calzado de plástico para bebé, fabricación, calzado de plástico para caballero, fabricación, calzado de plástico para dama, fabricación, calzado de plástico para niño, fabricación, calzado de plástico, fabricación, calzado de seguridad de plástico, fabricación, chanclas de plástico, fabricación, chancletas de plástico, fabricación, fábricas de calzado de plástico, pantufl	t	\N	\N
285	Fabricación de calzado de hule	botas de hule, fabricación, botines de hule, fabricación, calzado de hule para bebé, fabricación, calzado de hule para caballero, fabricación, calzado de hule para dama, fabricación, calzado de hule para niño, fabricación, calzado de hule, fabricación, calzado de seguridad de hule, fabricación, chanclas de hule, fabricación, chancletas de hule, fabricación, fábricas de calzado de hule, sandalias de hule, fabricación	t	\N	\N
286	Fabricación de huaraches y calzado de otro tipo de materiales	calzado con corte de vinil, fabricación, calzado tejido para bebé, fabricación, calzado tejido para caballero, fabricación, calzado tejido para dama, fabricación, calzado tejido para niño, fabricación, calzado tejido, fabricación, huaraches (calzado), fabricación, pantuflas tejidas, fabricación, sandalias tejidas, fabricación	t	\N	\N
586	Farmacias sin minisúper	abarrotes, comercio al por menor a través de métodos tradicionales o por internet en farmacias sin minisúper, aceites comestibles, comercio al por menor a través de métodos tradicionales o por internet en farmacias sin minisúper, aderezos envasados, comercio al por menor a través de métodos tradicionales o por internet en farmacias sin minisúper, agua oxigenada, comercio al por menor a través de métodos tradicionales o por internet en farmacias sin minisúper, agua purificada envasada, comercio a	t	\N	\N
287	Fabricación de bolsos de mano, maletas y similares	baúles de equipaje, fabricación, billeteras de cuero, piel y materiales sucedáneos, fabricación, bolsos de mano de cuero, piel y materiales sucedáneos, fabricación, bolsos de mano de lona, fabricación, bolsos de mano de tela, fabricación, carteras de cuero, piel y materiales sucedáneos, fabricación, cigarreras de cuero, piel y materiales sucedáneos, fabricación, equipaje de cuero, piel y materiales sucedáneos, fabricación, maletas de cuero, piel y materiales sucedáneos, fabricación, maletines de	t	\N	\N
288	Fabricación de otros productos de cuero, piel y materiales sucedáneos	accesorios de cuero para perro (collares, arneses, correas y bozales), fabricación, accesorios de uso industrial de cuero, piel y materiales sucedáneos, fabricación, alforjas de cuero, piel y materiales sucedáneos, fabricación, arcos de cuero para calzado, fabricación, arneses de cuero, fabricación, arreos de cuero, piel y materiales sucedáneos, fabricación, artesanías de cuero y piel, fabricación, artículos de cuero y piel para escritorio, fabricación, artículos de talabartería, fabricación, ar	t	\N	\N
289	Aserraderos integrados	aglutinados de madera, fabricación en aserraderos integrados, aserraderos integrados, barandales de madera, fabricación en aserraderos integrados, barriles, fabricación en aserraderos integrados, chapa de madera, fabricación en aserraderos integrados, cimbras de madera, fabricación en aserraderos integrados, closets de madera, fabricación en aserraderos integrados, contenedores de madera, fabricación en aserraderos integrados, contraventanas de madera, fabricación en aserraderos integrados, duel	t	\N	\N
290	Aserrado de tablas y tablones	abeto, aserrado a partir de madera en rollo, caoba, aserrado a partir de madera en rollo, cedro blanco, aserrado a partir de madera en rollo, cerezo, aserrado a partir de madera en rollo, ciprés, aserrado a partir de madera en rollo, ébano, aserrado a partir de madera en rollo, encino, aserrado a partir de madera en rollo, fresno, aserrado a partir de madera en rollo, haya, aserrado a partir de madera en rollo, listones de madera, aserrado a partir de madera en rollo, madera cepillada, fabricaci	t	\N	\N
291	Tratamiento de la madera y fabricación de postes y durmientes	creosotado de madera, durmientes de madera, fabricación a partir de madera aserrada, durmientes de madera, tratamiento, madera creosotada, fabricación, madera impregnada, fabricación, madera tratada, fabricación, pilotes de madera, fabricación, postes de madera, fabricación, postes de madera, tratamiento, productos de madera, impregnado, productos de madera, tratamiento, tratamiento de productos de madera	t	\N	\N
292	Fabricación de laminados y aglutinados de madera	aglutinados de madera, fabricación, chapa de madera blanda, fabricación, chapa de madera dura, fabricación, chapa de madera, fabricación, contrachapa con recubrimiento, fabricación, contrachapa de madera blanda, fabricación, contrachapa de madera dura, fabricación, contrachapa de madera, fabricación, estructuras de madera aglutinada, fabricación, estructuras de madera laminada, fabricación, hojas y tableros de aglomerado de madera, fabricación, laminados de madera de alta resistencia, fabricació	t	\N	\N
293	Fabricación de productos de madera para la construcción	andamios de madera, fabricación a partir de madera aserrada, armarios de madera, fabricación a partir de madera aserrada, barandales de madera, fabricación a partir de madera aserrada, bastidores de madera para puerta, fabricación a partir de madera aserrada, canceles de madera, fabricación a partir de madera aserrada, cimbras de madera, fabricación a partir de madera aserrada, closets de madera, fabricación a partir de madera aserrada, contrapuertas de madera, fabricación a partir de madera ase	t	\N	\N
294	Fabricación de productos para embalaje y envases de madera	alhajeros de madera, fabricación a partir de madera aserrada, aros de madera para barriles, fabricación a partir de madera aserrada, baldes de madera, fabricación a partir de madera aserrada, barricas de madera, fabricación a partir de madera aserrada, barriles de madera, fabricación a partir de madera aserrada, cajas de madera para embalaje, fabricación a partir de madera aserrada, cajas de madera para herramienta, fabricación a partir de madera aserrada, cajas decorativas de madera, fabricació	t	\N	\N
295	Fabricación de productos de materiales trenzables, excepto palma	artículos decorativos de bejuco, fabricación, artículos decorativos de carrizo, fabricación, artículos decorativos de materiales trenzables (excepto palma), fabricación, artículos decorativos de mimbre, fabricación, artículos decorativos de vara, fabricación, artículos ornamentales de bejuco, fabricación, artículos ornamentales de carrizo, fabricación, artículos ornamentales de materiales trenzables (excepto palma), fabricación, artículos ornamentales de mimbre, fabricación, artículos ornamental	t	\N	\N
296	Fabricación de artículos y utensilios de madera para el hogar	artículos y utensilios de madera para el hogar, fabricación a partir de madera aserrada, charolas de madera, fabricación a partir de madera aserrada, cucharas de madera, fabricación a partir de madera aserrada, ensaladeras de madera, fabricación a partir de madera aserrada, figuras decorativas de madera, fabricación a partir de madera aserrada, figuras ornamentales de madera, fabricación a partir de madera aserrada, fruteros de madera, fabricación a partir de madera aserrada, ganchos de madera p	t	\N	\N
297	Fabricación de productos de madera de uso industrial	bases de madera para reconocimientos y diplomas, fabricación a partir de madera aserrada, bases de madera para sillas, fabricación a partir de madera aserrada, bastidores de madera de uso industrial, fabricación a partir de madera aserrada, bloques de madera prensada para sastrería, fabricación a partir de madera aserrada, bujes de madera, fabricación a partir de madera aserrada, canillas de madera, fabricación a partir de madera aserrada, carretes de madera, fabricación a partir de madera aserr	t	\N	\N
298	Fabricación de otros productos de madera	asientos de madera para sanitario, fabricación, aulas de madera prefabricadas, fabricación partir de madera aserrada, boyas de corcho, fabricación, carbón vegetal, fabricación, casas de madera prefabricadas, fabricación a partir de madera aserrada, corcho, procesamiento, escaleras de mano de madera, fabricación a partir de madera aserrada, flotadores de corcho, fabricación, carcasas de madera para aparatos electrónicos, fabricación a partir de madera aserrada, garajes de madera prefabricados, fa	t	\N	\N
299	Fabricación de pulpa	celulosa de bagazo de caña, fabricación, celulosa mecánica, fabricación, celulosa química de madera, fabricación, pasta de desechos de cartón, fabricación, pasta de desechos de papel, fabricación, pasta de desechos textiles, fabricación, pasta de madera, fabricación, pulpa de desechos de cartón, fabricación, pulpa de desechos de papel, fabricación, pulpa de desechos textiles, fabricación, pulpa de materiales reciclados, fabricación, pulpa de paja, fabricación, pulpa mecánica, fabricación, pulpa 	t	\N	\N
667	Transporte colectivo urbano y suburbano de pasajeros en metro	pasajeros, transporte colectivo suburbano en metro, pasajeros, transporte colectivo suburbano en tren metropolitano, pasajeros, transporte colectivo urbano en metro	t	\N	\N
300	Fabricación de papel en plantas integradas	celulosa de bagazo de caña, fabricación en plantas de papel integradas, celulosa mecánica, fabricación en plantas de papel integradas, celulosa química de madera, fabricación en plantas de papel integradas, cuadernos, fabricación en plantas integradas, fieltros saturados, fabricación en plantas integradas, hojas de papel interdoblado, fabricación en plantas integradas, papel absorbente, fabricación en plantas integradas, papel albanene, fabricación en plantas integradas, papel amate, fabricación	t	\N	\N
301	Fabricación de papel a partir de pulpa	cartulina, fabricación a partir de pulpa comprada, fieltros saturados, fabricación a partir de pulpa comprada, hojas de papel interdoblado, fabricación a partir de pulpa comprada, papel absorbente, fabricación a partir de pulpa comprada, papel albanene, fabricación a partir de pulpa comprada, papel amate, fabricación a partir de pulpa comprada, papel arroz, fabricación a partir de pulpa comprada, papel asfaltado, fabricación a partir de pulpa comprada, papel bond, fabricación a partir de pulpa c	t	\N	\N
302	Fabricación de cartón en plantas integradas	archiveros de cartón, fabricación en plantas integradas, bobinas de cartón, fabricación en plantas integradas, cajas de cartón corrugado, fabricación en plantas integradas, cajas de cartón para regalo, fabricación en plantas integradas, cajas de cartón recubierto, fabricación en plantas integradas, cajas de cartón, fabricación en plantas integradas, canillas de cartón, fabricación en plantas integradas, carretes de cartón, fabricación en plantas integradas, cartón aglomerado, fabricación en plan	t	\N	\N
303	Fabricación de cartón y cartoncillo a partir de pulpa	cartón aglomerado, fabricación a partir de pulpa comprada, cartón alquitranado, fabricación a partir de pulpa comprada, cartón asfaltado, fabricación a partir de pulpa comprada, cartón blanco, fabricación a partir de pulpa comprada, cartón brístol, fabricación a partir de pulpa comprada, cartón corrugado, fabricación a partir de pulpa comprada, cartón cuché, fabricación a partir de pulpa comprada, cartón cuero o cuero artificial, fabricación a partir de pulpa comprada, cartón en rollo, fabricaci	t	\N	\N
304	Fabricación de envases de cartón	archiveros de cartón, fabricación a partir de cartón comprado, bobinas de cartón, fabricación a partir de cartón comprado, botes de cartón, fabricación a partir de cartón comprado, cajas de cartón corrugado, fabricación a partir de cartón comprado, cajas de cartón para embalaje, fabricación a partir de cartón comprado, cajas de cartón para productos agrícolas, fabricación a partir de cartón comprado, cajas de cartón para productos alimenticios, fabricación a partir de cartón comprado, cajas de c	t	\N	\N
305	Fabricación de bolsas de papel y productos celulósicos recubiertos y tratados	bolsas de papel aluminizado, fabricación a partir de papel comprado, bolsas de papel cuché, fabricación a partir de papel comprado, bolsas de papel estándar, fabricación a partir de papel comprado, bolsas de papel estucado, fabricación a partir de papel comprado, bolsas de papel impreso, fabricación a partir de papel comprado, bolsas de papel Kraft, fabricación a partir de papel comprado, bolsas de papel multicapas, fabricación a partir de papel comprado, bolsas de papel plastificado, fabricació	t	\N	\N
306	Fabricación de productos de papelería	blocs (artículos de papelería), fabricación a partir de papel comprado, carpetas de cartón, fabricación a partir de cartón comprado, cuadernos, fabricación a partir de papel comprado, folders, fabricación a partir de cartón comprado, hojas blancas, fabricación a partir de papel comprado, hojas de color, fabricación a partir de papel comprado, hojas de papel bond, fabricación a partir de papel comprado, hojas para carpeta, fabricación a partir de papel comprado, libretas, fabricación a partir de 	t	\N	\N
307	Fabricación de pañales desechables y productos sanitarios	cotonetes, fabricación, pañales desechables, fabricación, pañuelos desechables, fabricación, papel facial, fabricación a partir de papel comprado, papel higiénico, fabricación a partir de papel comprado, protectores para incontinencia, fabricación, servilletas desechables, fabricación a partir de papel comprado, tampones, fabricación, toallas de papel para cocina, fabricación a partir de papel comprado, toallas de papel para manos, fabricación a partir de papel comprado, toallas sanitarias, fabr	t	\N	\N
308	Fabricación de otros productos de cartón y papel	antifaces para fiesta, fabricación a partir de cartón comprado, artículos de cartón y papel moldeado, fabricación, artículos para fiestas infantiles, fabricación a partir de papel y cartón comprado, bases de cartón para fotografías, fabricación a partir de cartón comprado, cartón para huevo de cartón moldado, fabricación, charolas para huevo de cartón moldado, fabricación, confeti, fabricación a partir de papel comprado, conos de papel, fabricación a partir de papel comprado, figuras ornamentale	t	\N	\N
309	Impresión de libros, periódicos y revistas	anuarios, impresión, comics, impresión, diccionarios, impresión, enciclopedias, impresión, libros de bolsillo, impresión, libros de ficción, impresión, libros de referencia, impresión, libros de texto, impresión, libros escolares, impresión, libros infantiles, impresión, libros para adultos, impresión, libros para iluminar, impresión, libros profesionales, impresión, libros religiosos, impresión, libros, impresión, periódicos de información especializada, impresión, periódicos de información gen	t	\N	\N
310	Impresión de formas continuas y otros impresos	agendas, impresión, álbumes de estampas, impresión, álbumes para fotografía, fabricación, almanaques, impresión, atlas, impresión, boletines, impresión, boletos, impresión, bolsas, impresión, calcomanías, impresión, calendarios, impresión, carpetas, impresión, carteles, impresión, catálogos, impresión, ceniceros, impresión, cheques, impresión, comprobantes fiscales, impresión, credenciales, impresión, cupones, impresión, diplomas, impresión, directorios, impresión, encendedores, impresión, estam	t	\N	\N
311	Industrias conexas a la impresión	álbumes, encuadernación, clichés, elaboración, encuadernación con alambre, encuadernación en cuero, encuadernación rústica cosida, encuadernación rústica pegada, folletos, encuadernación, libros, encuadernación, negativos para prensa, preparación, placas flexográficas, elaboración, placas para fotograbado, elaboración, placas para grabado, elaboración, placas tipográficas, elaboración, post prensa, actividades de, preprensa, actividades de, productos impresos, biselado, productos impresos, borde	t	\N	\N
312	Refinación de petróleo	aceite crudo, refinación, aceites ácidos, fabricación en refinería, aceites aditivos, fabricación en refinería, aceites lubricantes, fabricación en refinería, aceites minerales, fabricación en refinería, ácidos nafténicos, fabricación en refinería, alquitrán, fabricación en refinería, asfalto, fabricación en refinería, azufre sólido, fabricación en refinería, benceno, fabricación en refinería, butileno, fabricación en refinería, cera de petróleo, fabricación en refinería, combustible para avión,	t	\N	\N
313	Fabricación de productos de asfalto	asfalto en rollo con gravilla, fabricación a partir de material asfáltico comprado, asfalto en rollo, fabricación a partir de material asfáltico comprado, asfalto para pisos, fabricación a partir de material asfáltico comprado, asfalto para techos, fabricación a partir de material asfáltico comprado, bloques de asfalto, fabricación a partir de material asfáltico comprado, cartón recubierto de asfalto, fabricación a partir de material asfáltico comprado, compuestos de alquitrán, fabricación a par	t	\N	\N
314	Fabricación de aceites y grasas lubricantes	aceite diésel, fabricación a partir de petróleo refinado, aceite para transmisión, fabricación a partir de petróleo refinado, aceite refrigerante, fabricación a partir de petróleo refinado, aceite regenerado, fabricación a partir de petróleo refinado, aceites automotrices, fabricación a partir de petróleo refinado, aceites de uso industrial, fabricación a partir de petróleo refinado, aceites hidráulicos, fabricación a partir de petróleo refinado, aceites lubricantes de uso automotriz, fabricació	t	\N	\N
315	Fabricación de coque y otros productos derivados del petróleo refinado y del carbón mineral	briquetas de antracita, fabricación, briquetas de carbón mineral, fabricación, briquetas de lignito, fabricación, briquetas, fabricación a partir de petróleo refinado, carbón de alquitrán, fabricación, cera de petróleo, fabricación a partir de petróleo refinado, coque de carbón mineral, fabricación, coque de petróleo, fabricación, gelatina (derivado del petróleo), fabricación a partir de petróleo refinado	t	\N	\N
316	Fabricación de petroquímicos básicos del gas natural y del petróleo refinado	benceno, fabricación a partir de gas natural, de hidrocarburos líquidos o de petróleo refinado, butadieno, fabricación a partir de gas natural, de hidrocarburos líquidos o de petróleo refinado, butano, fabricación a partir de gas natural, de hidrocarburos líquidos o de petróleo refinado, butileno, fabricación a partir de gas natural, de hidrocarburos líquidos o de petróleo refinado, cumeno, fabricación a partir de gas natural, de hidrocarburos líquidos o de petróleo refinado, estireno, fabricaci	t	\N	\N
317	Fabricación de gases industriales	acetileno, fabricación, aire comprimido, fabricación, aire líquido, fabricación, argón, fabricación, clorodifloruro de metano, fabricación, dióxido de carbono, fabricación, gases industriales comprimidos, fabricación, gases industriales fluorocarbonados, fabricación, gases industriales hidrocarbonados fluorinados, fabricación, gases industriales licuados, fabricación, gases industriales sólidos, fabricación, helio, fabricación, hidrógeno, fabricación, hielo seco (bióxido de carbono sólido), fabr	t	\N	\N
318	Fabricación de pigmentos y colorantes sintéticos	ácido arsénico, fabricación, colorantes ácidos sintéticos, fabricación, colorantes azoicos sintéticos, fabricación, colorantes cerámicos sintéticos, fabricación, colorantes de antraquinona, fabricación, colorantes de eosina, fabricación, colorantes de estilbenos, fabricación, colorantes de óxido hierro, fabricación, colorantes de pararosanilina, fabricación, colorantes de quinolina, fabricación, colorantes fluorescentes, fabricación, colorantes inorgánicos, fabricación, colorantes minerales, fab	t	\N	\N
319	Fabricación de otros productos químicos básicos inorgánicos	ácido bórico, fabricación, ácido bromhídrico, fabricación, ácido carbónico, fabricación, ácido cianhídrico, fabricación, ácido clorhídrico, fabricación, ácido clórico, fabricación, ácido clorocianúrico, fabricación, ácido cobaltoso, fabricación, ácido crómico, fabricación, ácido estánnico, fabricación, ácido fluobórico, fabricación, ácido fluorhídrico, fabricación, ácido hidrocianhídrico, fabricación, ácido hidroclorhídrico, fabricación, ácido hidrofluorhídrico, fabricación, ácido hipofosforoso,	t	\N	\N
320	Fabricación de otros productos químicos básicos orgánicos	aceite de alquitrán, fabricación, aceite de anilina, fabricación, aceite de creosota, fabricación, aceite de madera, fabricación, aceite de pino, fabricación, aceites esenciales sintéticos, fabricación, acetaldehído, fabricación, acetato amílico, fabricación, acetato de bencilo, fabricación, acetato de butilo, fabricación, acetato de cal natural, fabricación, acetato de calcio, fabricación, acetato de celulosa, fabricación, acetato de etilo, fabricación, acetato de isopropilo, fabricación, aceta	t	\N	\N
321	Fabricación de resinas sintéticas	adipatos, fabricación, aminoresinas, fabricación, compuestos de polipropileno, fabricación, compuestos de PVC, fabricación, compuestos plásticos, fabricación, copolímeros, fabricación, elastómeros no vulcanizables, fabricación, epiclorhidrina difenol, fabricación, homopolímeros, fabricación, materiales plastificantes, fabricación, piroxilina, fabricación, plásticos de carbohidratos, fabricación, plásticos de caseína, fabricación, plásticos de etil celulosa, fabricación, plásticos de soya, fabric	t	\N	\N
322	Fabricación de hules sintéticos	aceites vulcanizados, fabricación, compuestos de hule termoplástico, fabricación, copolímeros de butadieno-acrilonitrilo, fabricación, copolímeros de butadieno-estireno, fabricación, copolímeros de piridina-butadieno, fabricación, copolímeros de poliamida y poliéster, fabricación, elastómeros sintéticos, fabricación, elastómeros vulcanizables, fabricación, hule acrílico, fabricación, hule cloratado, fabricación, hule clorosulfatado, fabricación, hule de acrilato-butadieno, fabricación, hule de b	t	\N	\N
323	Fabricación de fibras químicas	fibramodal, fabricación, fibras acrílicas, fabricación, fibras armadías, fabricación, fibras artificiales, fabricación, fibras celulósicas, fabricación, fibras cuprocelulosas, fabricación, fibras de acetato desacetilado, fabricación, fibras de acetato, fabricación, fibras de acrilonitrilo, fabricación, fibras de alginato, fabricación, fibras de caseína, fabricación, fibras de celulosa, fabricación, fibras de cloro, fabricación, fibras de cloruro de polivinilideno, fabricación, fibras de cloruro 	t	\N	\N
324	Fabricación de fertilizantes y composta	abonos complejos, fabricación, abonos fosfatados, fabricación, abonos naturales, fabricación, abonos para suelo, fabricación, ácido fosfórico, fabricación, ácido nítrico, fabricación, amoniaco anhidro, fabricación, biofertlizantes, fabricación, composta, fabricación, compuestos de fertilizantes nitrogenados, fabricación, fertilizantes complejos, fabricación, fertilizantes con aminoácidos, fabricación, fertilizantes de liberación controlada, fabricación, fertilizantes foliares, fabricación, ferti	t	\N	\N
325	Fabricación de plaguicidas y otros agroquímicos, excepto fertilizantes y composta	acondicionadores de suelo agrícola, fabricación, arseniato de calcio formulado, fabricación, arseniato de cobre formulado, fabricación, arseniato de plomo formulado, fabricación, arsenito de calcio formulado, fabricación, arsenito de sodio formulado, fabricación, arsenitos formulados, fabricación, bactericidas agrícolas, fabricación, bioestimulantes agrícolas, fabricación, biofungicidas, fabricación, DDT (insecticida) formulado, fabricación, defoliantes, fabricación, desinfectantes agrícolas, fa	t	\N	\N
326	Fabricación de materias primas para la industria farmacéutica	acebutonol, fabricación, acenocumarol, fabricación, acetazolamida, fabricación, acetilcolina, fabricación, aciclovir, fabricación, ácido acetilsalicílico simple, fabricación, ácido ascórbico simple, fabricación, ácido barbitúrico simple, fabricación, ácido salicílico simple, fabricación, adenosina, fabricación, agentes antiarrítmicos, fabricación, alcaloides simples, fabricación, alfentanilo, fabricación, alicina, fabricación, almotriptán simple, fabricación, amantadina simple, fabricación, ambr	t	\N	\N
327	Fabricación de preparaciones farmacéuticas	aceites de uso medicinal, fabricación, ácido acetilsalicílico compuesto, fabricación, agar-agar (medio de cultivo), fabricación, agentes de diagnóstico, fabricación, agresinas compuestas, fabricación, agua para inyecciones, fabricación, alcohol de uso medicinal, fabricación, alérgenos compuestos, fabricación, analgésicos compuestos, fabricación, anestésicos compuestos, fabricación, anfetaminas compuestas, fabricación, ansiolíticos compuestos, fabricación, antiácidos compuestos, fabricación, anti	t	\N	\N
328	Fabricación de pinturas y recubrimientos	aceite para pinturas, fabricación, adelgazantes de laca, fabricación, adelgazantes de pintura preparados, fabricación, barniz para superficies, fabricación, base para barnices, fabricación, base para lacas, fabricación, base plástica para barnices, fabricación, base plástica para pinturas, fabricación, ceras para pintura, fabricación, colores en aceites excepto para artistas, fabricación, dispersantes coloidales para pintura, fabricación, dispersantes termoplásticos para pintura, fabricación, es	t	\N	\N
329	Fabricación de adhesivos	adhesivos de contacto, fabricación, adhesivos epóxicos, fabricación, adhesivos excepto dental, fabricación, adhesivos instantáneos, fabricación, adhesivos plásticos, fabricación, cemento (pegamento), fabricación, gomas-cemento, fabricación, lápiz adhesivo, fabricación, masillas para calafatear, fabricación, mastique, fabricación, pasta adhesiva, fabricación, pegamento amarillo, fabricación, pegamento blanco, fabricación, pegamento epóxico, fabricación, pegamentos de almidón, fabricación, pegamen	t	\N	\N
330	Fabricación de jabones, limpiadores y dentífricos	aceites solubles, (asistentes textiles), fabricación, acua-amonia doméstico, fabricación, agentes abrasivos para textiles, fabricación, agentes activos de actividad superficial, fabricación, agentes activos surfactantes, fabricación, agentes de acabado para piel, fabricación, agentes de acabado textil y cueros, fabricación, agentes de acabado textil, fabricación, agentes humectantes para textiles, fabricación, agentes tensoactivos, fabricación, almidón para lavandería, fabricación, antiespumante	t	\N	\N
331	Fabricación de cosméticos, perfumes y otras preparaciones de tocador	aceite para bebé, fabricación, aceites cosméticos, fabricación, acondicionadores para el cabello, fabricación, agua de colonia, fabricación, almohadillas perfumadas, fabricación, antitranspirantes, fabricación, barniz para uñas, fabricación, bloqueadores solares, fabricación, brillantinas para el cabello, fabricación, bronceadores solares, fabricación, burbujas para baño, fabricación, champús para cabello, fabricación, cosméticos, fabricación, cremas faciales y corporales, fabricación, cremas mo	t	\N	\N
332	Fabricación de tintas para impresión	cartuchos de tinta para impresión, fabricación, tintas acrílicas, fabricación, tintas ahuladas, fabricación, tintas de alto brillo, fabricación, tintas epóxicas fabricación, tintas para artes gráficas, fabricación, tintas para cojinete de sello, fabricación, tintas para impresión digital, fabricación, tintas para impresión flexográfica, fabricación, tintas para impresión litográfica, fabricación, tintas para impresión offset, fabricación, tintas para impresión tipográfica, fabricación, tintas pa	t	\N	\N
333	Fabricación de explosivos	ácido estífnico, fabricación, ácido pícrico (explosivo), fabricación, amatol (explosivo), fabricación, azida de mercurio (explosivo), fabricación, azida de plomo (explosivo), fabricación, azidas (explosivo), fabricación, cápsulas detonantes para fusibles de seguridad, fabricación, cápsulas explosivas, fabricación, carbohidratos nitrados (explosivo), fabricación, compuestos explosivos, fabricación, cordita (explosivo), fabricación, detonadores explosivos, fabricación, detonantes cordeau (explosiv	t	\N	\N
334	Fabricación de cerillos	cerillos, fabricación, fósforos (cerillos), fabricación	t	\N	\N
335	Fabricación de películas, placas y papel fotosensible para fotografía	blanqueadores para fotografía, fabricación, cintas para grabar películas cinematográficas, fabricación, estabilizadores para fotografía, fabricación, fijadores para fotografía, fabricación, gelatina para fotografía, fabricación, láminas sensibilizadas para rayos X, fabricación, papel sensibilizado para fotografía, fabricación, películas sensibilizadas para fotografía, fabricación, películas sensibilizadas para rayos-x, fabricación, placas para diapositivas, fabricación, placas sensibilizadas par	t	\N	\N
336	Fabricación de resinas de plásticos reciclados	resinas plásticas recicladas, fabricación, resinas recicladas de policarbonato (PC), fabricación, resinas recicladas de poliéster (PET), fabricación, resinas recicladas de poliestireno (PS), fabricación, resinas recicladas de polietileno de alta densidad (PEAD), fabricación, resinas recicladas de polipropileno (PP), fabricación, resinas recicladas de PVC, fabricación	t	\N	\N
337	Fabricación de otros productos químicos	aceite de anís, fabricación, aceite de bahía, fabricación, aceite de cedro, fabricación, aceite de citronela, fabricación, aceite de clavo, fabricación, aceite de eucalipto, fabricación, aceite de hierbabuena, fabricación, aceite de laurel, fabricación, aceite de lima, fabricación, aceite de limón, fabricación, aceite de menta, fabricación, aceite de naranja, fabricación, aceite de ricino, fabricación, aceite de toronja, fabricación, aceites automotrices sintéticos, fabricación, aceites esencial	t	\N	\N
338	Fabricación de bolsas y películas de plástico	bolsas de plástico en rollo, fabricación, bolsas de plástico para embutidos, fabricación, bolsas de plástico, fabricación, bolsas de polietileno (PE), fabricación, bolsas de polipropileno, fabricación de, hojas de plástico no sensibilizadas para fotografía, fabricación, hojas de poliéster, fabricación, hojas de polietileno (PE), fabricación, hojas de polipropileno (PP), fabricación, hojas de polivinilo, fabricación, hojas de vinil, fabricación, guantes desechables de plástico, fabricación, lamin	t	\N	\N
339	Fabricación de tubería y conexiones, y tubos para embalaje	conexiones de plástico para tubos, fabricación, conexiones de plástico rígido, fabricación, conexiones de poliestireno (PS), fabricación, conexiones de polietileno (PE), fabricación, conexiones de polipropileno (PP), fabricación, conexiones de PVC, fabricación, perfiles de plástico rígido, fabricación, perfiles de poliestireno (PS), fabricación, perfiles de polietileno (PE), fabricación, perfiles de polipropileno (PP), fabricación, perfiles de PVC, fabricación, tubería de plástico reforzado, fab	t	\N	\N
340	Fabricación de laminados de plástico	domos, fabricación, laminados de plástico corrugado, fabricación, laminados de plástico de alta densidad, fabricación, laminados de plástico de uso decorativo, fabricación, laminados de plástico de uso industrial, fabricación, laminados de plástico para la construcción, fabricación, laminados de plástico para paredes, fabricación, laminados de plástico para techo, fabricación, laminados de plástico, fabricación, laminados de acrílico, fabricación, laminados termoestables de plástico, fabricación	t	\N	\N
341	Fabricación de espumas y productos de poliestireno	acojinamientos de espuma de poliestireno (PS), fabricación, aislantes acústicos de espuma de poliestireno (PS), fabricación, aislantes térmicos de espuma de poliestireno (PS), fabricación, bloques aislantes de espuma de poliestireno (PS), fabricación, bloques de poliestireno expandido de alta densidad, fabricación, bovedilla de espuma de poliestireno (PS), fabricación, cajas de espuma de poliestireno (PS), fabricación, casetones de espuma de poliestireno (PS) para losa, fabricación, charolas de 	t	\N	\N
342	Fabricación de espumas y productos de uretano	acojinamientos de espuma de uretano, fabricación, aislantes acústicos de espuma de uretano, fabricación, aislantes térmicos de espuma de uretano, fabricación, almohadas de espuma de uretano, fabricación, asientos de espuma de uretano, fabricación, bloques de espuma de uretano, fabricación, empaques para embalaje de espuma de neopropeno, fabricación, empaques para embalaje de espuma de uretano, fabricación, espumas de poliestireno expandido (EPS), fabricación, espumas de polietileno (PE), fabrica	t	\N	\N
343	Fabricación de botellas de plástico	botellas de plástico, fabricación, botellones de plástico, fabricación, frascos de plástico, fabricación, garrafas de plástico, fabricación, garrafones de plástico, fabricación, preformas de botellas de plástico, fabricación	t	\N	\N
344	Fabricación de productos de plástico para el hogar con y sin reforzamiento	artículos de plástico para el hogar, fabricación, bandejas de plástico de uso doméstico, fabricación, biberones de plástico, fabricación, botes de plástico de uso doméstico, fabricación, cantimploras de plástico, fabricación, carpetas de plástico de uso doméstico, fabricación, cestos de plástico de uso doméstico, fabricación, charolas de plástico de uso doméstico, fabricación, cubetas de plástico de uso doméstico, fabricación, cubiertos de plástico, fabricación, cucharas de plástico, fabricación	t	\N	\N
345	Fabricación de autopartes de plástico con y sin reforzamiento	autopartes de fibra de vidrio, fabricación, autopartes de plástico, fabricación, botones de plástico para la industria automotriz, fabricación, calaveras de plástico para la industria automotriz, fabricación, carcasas de plástico para la industria automotriz, fabricación, cejas de plástico para faros para la industria automotriz, fabricación, coderas de plástico para la industria automotriz, fabricación, consolas de plástico para la industria automotriz, fabricación, contrapuertas de plástico pa	t	\N	\N
346	Fabricación de envases y contenedores de plástico para embalaje con y sin reforzamiento	bidones de plástico para embalaje, fabricación, botes de plástico para embalaje, fabricación, cajas de plástico para aves, fabricación, cajas de plástico para embalaje, fabricación, cajas de plástico para refrescos, fabricación, cestas de plástico para pollos, fabricación, charolas de plástico para embalaje, fabricación, contenedores colapsables de plástico, fabricación, contenedores de plástico para embalaje, fabricación, cubetas de plástico para embalaje, fabricación, cubos de plástico para em	t	\N	\N
347	Fabricación de otros productos de plástico de uso industrial sin reforzamiento	accesorios para baño de plástico sin reforzamiento, fabricación, aisladores de plástico sin reforzamiento, fabricación, artículos de plástico sin reforzamiento para laboratorio, fabricación, asientos para baño de plástico sin reforzamiento, fabricación, asientos para bicicleta de plástico sin reforzamiento, fabricación, bobinas de plástico sin reforzamiento, fabricación, carcasas de plástico sin reforzamiento para la industria electrónica, fabricación, carretes de plástico sin reforzamiento, fab	t	\N	\N
348	Fabricación de otros productos de plástico con reforzamiento	accesorios para baño de plástico con reforzamiento, fabricación, albercas de plástico con reforzamiento, fabricación, armazones de uso industrial de plástico con reforzamiento, fabricación, asientos para baño de plástico con reforzamiento, fabricación, bañeras de plástico con reforzamiento, fabricación, casas y edificios prefabricados de plástico reforzado, fabricación, casetas de plástico con reforzamiento, fabricación, contraventanas de plástico con reforzamiento, fabricación, cubiertas de plá	t	\N	\N
349	Fabricación de otros productos de plástico sin reforzamiento	accesorios para plomería de plástico, fabricación, arandelas de plástico, fabricación, arillos de plástico para encuadernación, fabricación, atomizadores de plástico, fabricación, balsas inflables de plástico, fabricación, bases para macetas de plástico, fabricación, botes inflables de plástico, fabricación, cigarreras de plástico, fabricación, colchones inflables para alberca de plástico, fabricación, embudos de plástico de uso industrial sin reforzamiento, fabricación, exhibidores de acrílico,	t	\N	\N
350	Fabricación de llantas y cámaras	bandas de rodadura para revitalización, fabricación, cámaras neumáticas, fabricación, corbatas para llantas, fabricación, hule piso para llantas, fabricación, llantas convencionales, fabricación, llantas de carros para expender productos, fabricación, llantas neumáticas, fabricación, llantas para automóviles, fabricación, llantas para aviones, fabricación, llantas para bicicletas, fabricación, llantas para camión, fabricación, llantas para camionetas, fabricación, llantas para carretillas, fabri	t	\N	\N
351	Revitalización de llantas	cámaras, revulcanizado, cubiertas de llantas, renovación, llantas, recauchutado, llantas, revitalización	t	\N	\N
352	Fabricación de bandas y mangueras de hule y de plástico	bandas de hule de uso industrial, fabricación, bandas de hule para la industria automotriz, fabricación, bandas de hule, fabricación, bandas de plástico de uso industrial, fabricación, bandas de plástico para la industria automotriz, fabricación, bandas de plástico, fabricación, correas de hule para transmisión, fabricación, mangueras de hule de uso industrial, fabricación, mangueras de hule para aspiradoras, fabricación, mangueras de hule para hidrantes, fabricación, mangueras de hule para uso 	t	\N	\N
353	Fabricación de otros productos de hule	arandelas de hule, fabricación, baberos de hule, fabricación, balsas inflables de hule, fabricación, boquillas de hule, fabricación, botes inflables de hule, fabricación, calzones de hule para bebé, fabricación, capuchones de hule, fabricación, chalecos inflables de hule, fabricación, colchones inflables de hule, fabricación, condones, fabricación, conexiones de hule, fabricación, cubiertas de hule, fabricación, dedales de hule, fabricación, diafragmas de hule vulcanizado, excepto diafragmas par	t	\N	\N
354	Fabricación de artículos de alfarería, porcelana y loza	abrazaderas de porcelana, fabricación, aislantes eléctricos de cerámica, fabricación, aislantes eléctricos de porcelana, fabricación, alhajeros de barro, fabricación, alhajeros de cerámica, fabricación, alhajeros de porcelana, fabricación, apagadores de cerámica, fabricación, arcilla, obtención integrada con la fabricación de productos de alfarería, porcelana y loza, artesanías de barro, fabricación, artesanías de cerámica, fabricación, artículos de alfarería de uso doméstico, fabricación, artíc	t	\N	\N
355	Fabricación de muebles de baño	accesorios para baño de cerámica, fabricación, bidés de cerámica, fabricación, cepilleros de cerámica, fabricación, depósitos de agua para inodoro de cerámica, fabricación, inodoros de cerámica, fabricación, jaboneras de cerámica, fabricación, lavabos de cerámica, fabricación, mingitorios de cerámica, fabricación, muebles de baño de cerámica, fabricación, pedestales para lavabo de cerámica, fabricación, percheros para baño de cerámica, fabricación, sanitarios de cerámica, fabricación, tinas para	t	\N	\N
356	Fabricación de ladrillos no refractarios	bloques de arcilla no refractaria, fabricación, celosías de arcilla no refractaria, fabricación, ladrillos de adobe, fabricación, ladrillos de arcilla no refractaria, fabricación, ladrillos de fibrocemento, fabricación, ladrillos decorativos de arcilla no refractaria, fabricación, ladrillos huecos de arcilla no refractaria, fabricación, ladrillos macizos de arcilla no refractaria, fabricación, ladrillos no refractarios integrada con la obtención de arcilla, fabricación, ladrillos no refractarios	t	\N	\N
357	Fabricación de azulejos y losetas no refractarias	azulejos de cerámica, fabricación, baldosas de cerámica, fabricación, cenefas de cerámica, fabricación, losetas de cerámica, fabricación, losetas industriales de cerámica, fabricación, losetas no refractarias, fabricación, mosaicos no refractarios, fabricación, pavimento porcelánico, fabricación, zoclos de cerámica, fabricación	t	\N	\N
358	Fabricación de productos refractarios	arcilla para fundición, fabricación, arcilla refractaria, fabricación, azulejos refractarios, fabricación, bloques refractarios, fabricación, cemento aluminoso, fabricación, cemento refractario no arcilloso, fabricación, cemento refractario, fabricación, crisoles de grafito, fabricación, crisoles de magnesio, fabricación, crisoles de silicio, fabricación, crisoles refractarios, fabricación, ladrillos de bauxita, fabricación, ladrillos de carburo de silicio, fabricación, ladrillos de silicio, fab	t	\N	\N
359	Fabricación de vidrio	cristal flotado, fabricación, cristal inastillable, fabricación, hojas de vidrio, fabricación, placas de vidrio, fabricación, productos de vidrio, fabricación integrada con la producción de vidrio, vidrio (blanco) para uso oftálmico, fabricación, vidrio aislante, fabricación, vidrio blindado, fabricación, vidrio borosilicatado, fabricación, vidrio colado, fabricación, vidrio de color, fabricación, vidrio de sílice, fabricación, vidrio de uso automotriz, fabricación, vidrio en planchas, fabricaci	t	\N	\N
360	Fabricación de espejos	espejos cóncavos, fabricación, espejos convexos, fabricación, espejos de seguridad, fabricación, espejos planos, fabricación	t	\N	\N
361	Fabricación de envases y ampolletas de vidrio	botellas de vidrio, fabricación, envases de vidrio, fabricación, frascos de vidrio, fabricación, garrafas de vidrio, fabricación, garrafones de vidrio, fabricación	t	\N	\N
362	Fabricación de fibra de vidrio	cables de fibra de vidrio sin aislar, fabricación, fibra óptica de vidrio, fabricación, fibra de vidrio, fabricación, lana de vidrio, fabricación	t	\N	\N
363	Fabricación de artículos de vidrio de uso doméstico	adornos de vidrio, fabricación, alhajeros de vidrio, fabricación, artesanías de vidrio, fabricación, artículos de vidrio de uso doméstico, fabricación, azucareras de vidrio, fabricación, bomboneras de vidrio, fabricación, botaneros de vidrio, fabricación, cafeteras de vidrio, fabricación, ceniceros de vidrio, fabricación, charolas de vidrio, fabricación, copas de cristal, fabricación, copas de vidrio, fabricación, cristalería de uso doméstico, fabricación, cubiertas de vidrio, fabricación, dulce	t	\N	\N
364	Fabricación de artículos de vidrio de uso industrial y comercial	accesorios para baño de vidrio, fabricación, aislantes eléctricos de vidrio, fabricación, ampollas de vidrio para termos, fabricación, artículos de vidrio de uso comercial, fabricación, artículos de vidrio de uso industrial, fabricación, artículos de vidrio para la industria eléctrica, fabricación, artículos de vidrio para la industria electrónica, fabricación, artículos de vidrio para laboratorio, fabricación, artículos de vidrio para señalización, fabricación, bloques de vidrio, fabricación, b	t	\N	\N
365	Fabricación de otros productos de vidrio	productos de vidrio emplomado, fabricación, vidrio esmerilado, fabricación, vidrio, decoración, vidrios biselados, fabricación, vitrales, fabricación	t	\N	\N
366	Fabricación de cemento y productos a base de cemento en plantas integradas	cemento antiácido, fabricación, cemento blanco, fabricación, cemento clínker, fabricación, cemento de escorias, fabricación, cemento de fraguado lento, fabricación, cemento de fraguado rápido, fabricación, cemento expansivo, fabricación, cemento fundido, fabricación, cemento gris, fabricación, cemento hidráulico, fabricación, cemento magnésico, fabricación, cemento metalúrgico, fabricación, cemento natural, fabricación, cemento para hormigón, fabricación, cemento para la construcción, fabricació	t	\N	\N
367	Fabricación de concreto	concreto bombeable, fabricación, concreto de alta resistencia, fabricación, concreto de fraguado acelerado, fabricación, concreto de fraguado retardado, fabricación, concreto de relleno, fabricación, concreto premezclado, fabricación, concreto, fabricación, hormigón, fabricación	t	\N	\N
368	Fabricación de tubos y bloques de cemento y concreto	adocretos, fabricación, adoquines de concreto, fabricación, bloques de concreto, fabricación, bloques huecos de concreto, fabricación, bloques macizos de concreto, fabricación, celosías de concreto, fabricación, codos de concreto, fabricación, ladrillos de concreto, fabricación, tabicones de concreto, fabricación, tabiques de concreto, fabricación, tuberías de concreto, fabricación, tubos de concreto para alcantarillado, fabricación, tubos de concreto para drenaje, fabricación, tubos de concreto	t	\N	\N
369	Fabricación de productos preesforzados de concreto	columnas preesforzadas de concreto, fabricación, componentes estructurales preesforzados de concreto, fabricación, durmientes preesforzados de concreto, fabricación, elementos de entrepiso preesforzados de concreto, fabricación, elementos estructurales preesforzados de concreto, fabricación, losas preesforzadas de concreto para entrepisos y azoteas, fabricación, losas preesforzadas de concreto, fabricación, muros preesforzados de concreto, fabricación, partes de puentes preesforzados de concreto	t	\N	\N
668	Transporte colectivo urbano y suburbano de pasajeros en autobuses que transitan en carril exclusivo	pasajeros, transporte colectivo suburbano en autobuses que transitan en carril exclusivo, pasajeros, transporte colectivo urbano en autobuses que transitan en carril exclusivo	t	\N	\N
370	Fabricación de otros productos de cemento y concreto	anclas de concreto, fabricación, arbotantes de concreto, fabricación, bancas de concreto, fabricación, bases de concreto para luminarias, fabricación, bases de concreto para transformadores, fabricación, bóvedas de concreto para transformadores, fabricación, columnas de concreto excepto preesforzadas, fabricación, cornisas de concreto, fabricación, criptas de concreto, fabricación, escalones de concreto, fabricación, estatuas de hormigón, fabricación, fuentes de concreto, fabricación, gárgolas d	t	\N	\N
371	Fabricación de cal	cal aérea, fabricación, cal agrícola, fabricación, cal apagada, fabricación, cal hidratada (calhidra), fabricación, cal hidráulica, fabricación, cal horneada, fabricación, cal magra, fabricación, cal rápida, fabricación, cal terraplén, fabricación, cal viva, fabricación, cal, fabricación, dolomita calcinada, fabricación	t	\N	\N
372	Fabricación de yeso y productos de yeso	artículos decorativos de yeso, fabricación, columnas de yeso, fabricación, compuestos de yeso para uniones, fabricación, estatuillas de yeso, fabricación, figuras ornamentales de yeso de parís, fabricación, figuras ornamentales de yeso, fabricación, fuentes de yeso de parís, fabricación, gargantas para iluminación de yeso, fabricación, malla con yeso, fabricación, materiales para construcción a base de yeso, fabricación, molduras de yeso, fabricación, paneles acústicos de yeso, fabricación, pane	t	\N	\N
373	Fabricación de productos abrasivos	abrasivos aglomerados de carburo de silicio, fabricación, abrasivos aglomerados de óxido de aluminio, fabricación, abrasivos en grano, fabricación, abrasivos en polvo, fabricación, bandas abrasivas, fabricación, bandas de lija, fabricación, bolas de molino, fabricación, discos abrasivos, fabricación, esmeriles de rueda, fabricación, hojas abrasivas de cuarzo, fabricación, hojas abrasivas, fabricación, hojas de esmeril, fabricación, lijas, fabricación, piedras molares, fabricación, piedras pómez,	t	\N	\N
374	Fabricación de productos a base de piedras de cantera	accesorios para baño de mármol, fabricación, altares de granito, fabricación, altares de mármol, fabricación, artesanías de ónix, fabricación, balaustres de piedras de cantera, fabricación, bases para lámparas de piedras de cantera, fabricación, bases para muebles de granito, fabricación, bases para muebles de mármol, fabricación, bases para muebles de obsidiana, fabricación, bases para muebles de ónix, fabricación, bases para muebles de piedras de cantera, fabricación, bordillos de granito, fab	t	\N	\N
375	Fabricación de otros productos a base de minerales no metálicos	arcilla activada por desecado, fabricación, asbesto comprimido, fabricación, bario, procesamiento posterior al beneficio, barita, procesamiento posterior al beneficio, caolín, procesamiento posterior al beneficio, cintas de asbesto, fabricación, clinca, fabricación, cordones de asbesto, fabricación, esquisto expandido, fabricación, feldespato, procesamiento posterior al beneficio, gemas sintéticas, fabricación, grafito natural pulverizado y refinado, fabricación, láminas de asbesto, fabricación,	t	\N	\N
376	Complejos siderúrgicos	acero al carbono, fabricación en complejos siderúrgicos, acero aleado de gran resistencia, fabricación en complejos siderúrgicos, acero corrugado, fabricación en complejos siderúrgicos, acero de baja radiación, fabricación en complejos siderúrgicos, acero de gran elasticidad, fabricación en complejos siderúrgicos, acero de horno eléctrico, fabricación en complejos siderúrgicos, acero en polvo, fabricación en complejos siderúrgicos, acero forjado, fabricación en complejos siderúrgicos, acero inox	t	\N	\N
377	Fabricación de desbastes primarios y ferroaleaciones	biletes, fabricación a partir de arrabio comprado, desbastes primarios y ferroaleaciones, fabricación, desbastes primarios, fabricación a partir del arrabio comprado, ferroaleaciones, fabricación a partir de material comprado, ferro-columbio, fabricación a partir de material comprado, ferro-cromo, fabricación a partir de material comprado, ferro-fósforo, fabricación a partir de material comprado, ferro-manganeso, fabricación a partir de material comprado, ferro-molibdeno, fabricación a partir de	t	\N	\N
378	Fabricación de tubos y postes de hierro y acero	conexiones de metal para tubería, fabricación a partir de acero comprado, postes de metal, fabricación a partir de metal comprado, postes, fabricación a partir de acero comprado, postes, fabricación a partir de hierro comprado, tubos con costura, fabricación a partir de hierro y acero comprados, tubos de acero al carbón, fabricación a partir de acero comprados, tubos de acero forjado, fabricación a partir de hierro y acero comprados, tubos de acero inoxidable, fabricación a partir de hierro y ac	t	\N	\N
379	Fabricación de otros productos de hierro y acero	alambre galvanizado, fabricación a partir de acero comprado, alambrón de acero de alto carbono, fabricación a partir de hierro y acero comprados, alambrón de acero de bajo carbono, fabricación a partir de hierro y acero comprados, alambrón, fabricación a partir de acero comprado, ángulos, fabricación a partir de hierro y acero comprados, armaduras de varilla para construcción, fabricación a partir de hierro y acero comprados, barras huecas, fabricación a partir de hierro y acero comprados, barra	t	\N	\N
380	Industria básica del aluminio	alambrón de aluminio, fabricación, aleaciones a base de aluminio, fabricación, aleaciones a base de aluminio, recuperación, alúmina, refinación, aluminio de uso industrial, fabricación, aluminio en rollo, fabricación, aluminio granulado, fabricación, aluminio, fabricación a partir de alúmina, aluminio, fabricación a partir de desechos de aluminio, aluminio, recuperación, ángulos de aluminio, fabricación, barras de aluminio, fabricación, barrotes de aluminio, fabricación, cables de aluminio, fabr	t	\N	\N
381	Fundición y refinación de cobre	aleaciones a base de cobre, fabricación, cobre blíster, fabricación, cobre electrolítico, fabricación, cobre-berilio, fabricación, cobre-estaño (bronce), fabricación, cobre-manganeso, fabricación, cobre-níquel, fabricación, cobre-plomo, fabricación, cobre-zinc (latón), fabricación, lingotes de cobre, fabricación, planchones de cobre, fabricación, productos de laminación primaria del cobre, fabricación, tochos de cobre, fabricación	t	\N	\N
382	Fundición y refinación de metales preciosos	aleaciones a base de oro, fabricación, aleaciones a base de osmio, fabricación, aleaciones a base de paladio, fabricación, aleaciones a base de plata, fabricación, aleaciones a base de platino, fabricación, aleaciones a base de rodio, fabricación, iridio, fundición y refinación, lingotes de oro, fabricación, lingotes de paladio, fabricación, lingotes de plata, fabricación, lingotes de platino, fabricación, metales preciosos, fundición y refinación, oro, fundición y refinación, osmio, fundición y	t	\N	\N
383	Fundición y refinación de otros metales no ferrosos	aleaciones a base de antimonio, fabricación, aleaciones a base de berilio, fabricación, aleaciones a base de bismuto, fabricación, aleaciones a base de cadmio, fabricación, aleaciones a base de circonio, fabricación, aleaciones a base de cobalto, fabricación, aleaciones a base de columbio, fabricación, aleaciones a base de cromo, fabricación, aleaciones a base de estaño, fabricación, aleaciones a base de estroncio, fabricación, aleaciones a base de germanio, fabricación, aleaciones a base de man	t	\N	\N
384	Laminación secundaria de cobre	alambre de cobre, fabricación, aleaciones a base de cobre, recuperación, ángulos de cobre, fabricación, barras de cobre, fabricación, barras de latón, fabricación, cables de cobre, fabricación, canaletas de cobre, fabricación, cobre granulado, fabricación, cobre, recuperación, conexiones de cobre, fabricación, escamas de cobre, fabricación, granalla de cobre, fabricación, hojas de cobre, fabricación, láminas de cobre, fabricación, malla de alambre de cobre, fabricación, perfiles de cobre, fabric	t	\N	\N
385	Laminación secundaria de otros metales no ferrosos	alambre de antimonio, fabricación, alambre de berilio, fabricación, alambre de bismuto, fabricación, alambre de cadmio, fabricación, alambre de circonio, fabricación, alambre de columbio, fabricación, alambre de cromo, fabricación, alambre de estaño, fabricación, alambre de estroncio, fabricación, alambre de germanio, fabricación, alambre de iridio, fabricación, alambre de litio, fabricación, alambre de manganeso, fabricación, alambre de metales preciosos, fabricación, alambre de molibdeno, fabr	t	\N	\N
386	Moldeo por fundición de piezas de hierro y acero	acero comprado, fundición invertida, acero comprado, moldeo por fundición, acero gris, moldeo por fundición, fierro maleable, moldeo por fundición, lingoteras, moldeo por fundición, piezas de acero, moldeo por fundición, piezas de hierro, moldeo por fundición, piezas de semiacero, moldeo por fundición	t	\N	\N
387	Moldeo por fundición de piezas metálicas no ferrosas	aleaciones a base de cobre, moldeo por fundición, aluminio comprado, moldeo por fundición, cobre comprado, moldeo por fundición, piezas con aleaciones de aluminio, moldeo por fundición, piezas de aluminio, moldeo por fundición, piezas de berilio, moldeo por fundición, piezas de bronce, moldeo por fundición, piezas de cobre, moldeo por fundición, piezas de latón, moldeo por fundición, piezas de magnesio, moldeo por fundición, piezas de metales no ferrosos, moldeo por fundición, piezas de níquel, 	t	\N	\N
388	Fabricación de productos metálicos forjados y troquelados	casquillos de metal estampados y troquelados, fabricación, corcholatas, fabricación, forjas de acero para prensa, fabricación, forjas de aluminio, fabricación, forjas de hierro para prensa, fabricación, forjas de metales no ferrosos, fabricación, forjas de metales, fabricación, forjas para accesorios de plomería, fabricación, material de fricción, fabricación a partir de pulvimetal, piezas estampadas de acero, fabricación, piezas estampadas de aluminio, fabricación, piezas estampadas de hierro, 	t	\N	\N
389	Fabricación de herramientas de mano metálicas sin motor	accesorios intercambiables para herramientas de mano, fabricación, alicates, fabricación, amoladoras manuales sin motor, fabricación, arcos para seguetas, fabricación, atornilladores manuales sin motor, fabricación, avellanadores manuales, fabricación, barras de alineación (herramienta de mano), fabricación, barrenas de mano sin motor, fabricación, barretas, fabricación, bayonetas, fabricación, bieldos, fabricación, brocas para herramientas de mano, fabricación, buriles, fabricación, calibradore	t	\N	\N
390	Fabricación de utensilios de cocina metálicos	abrelatas manuales, fabricación, baterías de cocina de acero inoxidable, fabricación, baterías de cocina de aluminio, fabricación, baterías de cocina de metal, fabricación, baterías de cocina de peltre, fabricación, batidores manuales de acero inoxidable, fabricación, cacerolas de acero inoxidable, fabricación, cacerolas de aluminio, fabricación, cacerolas de peltre, fabricación, cacerolas, fabricación, cascanueces, fabricación, charolas de acero inoxidable, fabricación, charolas de aluminio, fa	t	\N	\N
391	Fabricación de estructuras metálicas	andamios de metal, fabricación, armazones para la construcción de placa metálica, fabricación, barras reforzadas para concreto, fabricación, bastidores metálicos, fabricación, canaletas de placa metálica, fabricación, casas y edificios de metal prefabricados, fabricación, cobertizos de metal prefabricados, fabricación, columnas estructurales metálicas, fabricación, compuertas metálicas, fabricación, cubiertas estructurales de metal, fabricación, cubiertas flotantes de placa metálica, fabricación	t	\N	\N
392	Fabricación de productos de herrería	balconería de aluminio, fabricación, balconería de hierro y acero, fabricación, barandales de aluminio, fabricación, barandales de hierro y acero, fabricación, barandillas de tubo metálico, fabricación, cancelería de aluminio, fabricación, cercas metálicas, fabricación, columpios de hierro y acero, fabricación, contrapuertas de hierro y acero, fabricación, contraventanas de hierro y acero, fabricación, cornisas de lámina de metal, fabricación, corrales de hierro y acero, fabricación, cortinas de	t	\N	\N
393	Fabricación de calderas industriales	absorbedores de calor, fabricación, absorbedores de gas, fabricación, acumuladores de vapor para calderas industriales, fabricación, calderas (excepto de calefacción central), fabricación, calderas acuotubulares, fabricación, calderas de agua caliente, fabricación, calderas de alta presión, fabricación, calderas de fluido térmico, fabricación, calderas de potencia, fabricación, calderas de recuperación de calor, fabricación, calderas de recuperación de gases, fabricación, calderas de sobrecalent	t	\N	\N
394	Fabricación de tanques metálicos de calibre grueso	autoclaves de tipo industrial, fabricación, cisternas metálicas, fabricación, columnas fraccionadoras, fabricación, hervidores metálicos de calibre grueso, fabricación, marmitas metálicas, fabricación, ollas metálicas de calibre grueso de uso industrial, fabricación, recipientes metálicos de calibre grueso para altas presiones, fabricación, silos metálicos excepto agrícolas, fabricación, tanques (cilindros) para gas, fabricación, tanques atmosféricos de acero al carbón, fabricación, tanques atmo	t	\N	\N
395	Fabricación de envases metálicos de calibre ligero	bidones metálicos para embalaje, fabricación, botes de aluminio de uso industrial, fabricación, botes de aluminio para embalaje de alimentos y bebidas, fabricación, botes de aluminio para embalaje de productos farmacéuticos, fabricación, botes de aluminio para embalaje industrial, fabricación, botes de metal para embalaje al vacío, fabricación, botes de metal para embalaje de alimentos y bebidas, fabricación, botes de metal para embalaje, fabricación, cajas de hojalata para embalaje, fabricación	t	\N	\N
396	Fabricación de herrajes y cerraduras	bisagras, fabricación, candados, fabricación, cerraduras automáticas, fabricación, cerraduras de alta seguridad, fabricación, cerraduras de barra, fabricación, cerraduras de caja fuerte, fabricación, cerraduras de caja, fabricación, cerraduras de manija, fabricación, cerraduras de pomo, fabricación, cerraduras electromagnéticas, fabricación, cerraduras electrónicas, fabricación, cerraduras monederas, fabricación, cerraduras para automóviles, fabricación, cerraduras para bóvedas, fabricación, cer	t	\N	\N
703	Almacenamiento con refrigeración	almacenamiento con refrigeración, almacenamiento en bodegas con refrigeración, almacenamiento en cámaras frigoríficas, almacenamiento en refrigeradores, carga empacada, almacenamiento con refrigeración, productos congelados, almacenamiento, productos de granjas, almacenamiento refrigerado, productos perecederos, almacenamiento con refrigeración, productos refrigerados, almacenamiento	t	\N	\N
397	Fabricación de alambre, productos de alambre y resortes	alambre de púas de alta tensión, fabricación a partir de alambre comprado, alambre de púas, fabricación a partir de alambre comprado, alambre laminado, fabricación a partir de alambre comprado, alambre para amarres, fabricación a partir de alambre comprado, alambre recocido, fabricación a partir de alambre comprado, alambre semiflecha, fabricación a partir de alambre comprado, alambrón galvanizado, fabricación a partir de alambre comprado, alcayatas, fabricación, anaqueles de alambre, fabricació	t	\N	\N
398	Maquinado de piezas para maquinaria y equipo en general	bridas, maquinado, brocas, maquinado, bujes para maquinaria, maquinado, cilindros para maquinaria, maquinado, coples para maquinaria y equipo, maquinado, cremalleras para maquinaria y equipo, maquinado, ejes para maquinaria, maquinado, engranes y piñones para maquinaria, maquinado, espárragos de metal, fabricación, flechas para maquinaria, maquinado, impresión sobre pedido de productos en tercera dimensión (impresión 3D), maquinado de piezas nuevas y usadas que combinan materiales como metal, pl	t	\N	\N
399	Fabricación de tornillos, tuercas, remaches y similares	arandelas de metal, fabricación, birlos de metal, fabricación, clavijas de metal (sujetadores), fabricación, pernos metálicos, fabricación, pijas de metal, fabricación, remaches de metal, fabricación, rondanas de metal, fabricación, sujetadores de metal, fabricación, tornillería de metal, fabricación, tornillos de acero, fabricación, tornillos de aluminio, fabricación, tornillos de bronce, fabricación, tornillos de latón, fabricación, tornillos para madera, fabricación, tornillos para metal, fab	t	\N	\N
400	Recubrimientos y terminados metálicos	anodizado de piezas metálicas, aplicación de pintura electrostática en polvo en piezas metálicas, barnizado de piezas metálicas, bonderizado de piezas metálicas, bruñido de piezas metálicas, cadmizado de piezas metálicas, chapeado de piezas metálicas con metales preciosos, cobrizado de piezas metálicas, cortado de piezas metálicas hecho sobre pedido, cortado y doblez de piezas metálicas hecho sobre pedido, corte de rollos metálicos en cintas y láminas, cromado de piezas metálicas, decapado de pi	t	\N	\N
401	Fabricación de válvulas metálicas	acopladores metálicos para válvulas, fabricación, aspersores para césped, fabricación, boquillas metálicas para mangueras de jardín, fabricación, boquillas metálicas para spray, fabricación, conectores metálicos para válvulas, fabricación, coples metálicos para válvulas, fabricación, grifos metálicos, fabricación, hidrantes para incendios, fabricación, llaves de paso, fabricación, sifones, fabricación, válvulas metálicas automáticas, fabricación, válvulas metálicas de aguja, fabricación, válvula	t	\N	\N
402	Fabricación de baleros o rodamientos	baleros industriales, fabricación, bolas de acero, fabricación, bordes para cojinete, fabricación, chumaceras industriales, fabricación, cojinetes para baleros o rodamientos industriales, fabricación, collarines industriales, fabricación, rodamientos axiales, fabricación, rodamientos cónicos, fabricación, rodamientos de aguja, fabricación, rodamientos de bola, fabricación, rodamientos de cilindro, fabricación, rodamientos de rodillo cilíndrico, fabricación, rodamientos de rodillo de leva, fabric	t	\N	\N
403	Fabricación de otros productos metálicos	abanicos metálicos de mano, fabricación, abrazaderas metálicas, excepto para cableado eléctrico, fabricación, accesorios de metal para baño, fabricación, alcantarillas metálicas, fabricación, ametralladoras, fabricación, armas de fuego y sus partes, fabricación, armas deportivas y sus partes, fabricación, armazones metálicos para lámparas, fabricación, armazones metálicos para paraguas, fabricación, balas de plomo, fabricación, bañeras de metal, fabricación, botes de metal para basura, fabricaci	t	\N	\N
404	Fabricación de maquinaria y equipo agrícola	abonadoras de uso agrícola, fabricación, apiladoras de granos agrícolas, fabricación, apisonadoras de terreno agrícolas, fabricación, arados para actividades agrícolas, fabricación, aspersores agrícolas, fabricación, aspersores para productos agrícolas, fabricación, azadones agrícolas, fabricación, bordeadoras de pasto, fabricación, cargadores de productos agrícolas, fabricación, carretillas para césped, fabricación, clasificadoras de productos agrícolas, fabricación, cortadoras con motor para j	t	\N	\N
405	Fabricación de maquinaria y equipo pecuario	abrevaderos, fabricación, alimentadores de uso pecuario, fabricación, baños maría de uso pecuario, fabricación, bebederos de uso pecuario, fabricación, bretes de uso pecuario, fabricación, castradores, fabricación, corrales de uso pecuario, fabricación, cortapatas de uso pecuario, fabricación, desolladoras de uso pecuario, fabricación, equipo para uso pecuario, fabricación, esquiladoras eléctricas de uso pecuario, fabricación, incubadoras para actividades pecuarias, fabricación, maquinaria y equ	t	\N	\N
406	Fabricación de maquinaria y equipo para la construcción	ahoyadores para la construcción, fabricación, alisadoras para la construcción, fabricación, allanadoras para la construcción, fabricación, apisonadoras para la construcción, fabricación, aplanadoras de asfalto, fabricación, barrenas para la construcción, fabricación, bloqueras para la industria de la construcción, fabricación, brocas para la construcción, fabricación, bulldozers para construcción, fabricación, calentadores de asfalto para la construcción, fabricación, cargadores de pala para la 	t	\N	\N
407	Fabricación de maquinaria y equipo para la industria extractiva	alimentadores de minerales y agregados, fabricación, amalgamadores para minería, fabricación, barrenas para minería, fabricación, brocas para perforación subterránea, fabricación, carretillas para minería, fabricación, carros de volteo para minería, fabricación, carros subterráneos para transportar minerales, fabricación, clasificadores de minerales, fabricación, cortadoras de minerales, fabricación, equipo para campos de petróleo y gas, fabricación, equipo para perforación minera, fabricación, 	t	\N	\N
408	Fabricación de maquinaria y equipo para la industria de la madera	aserradoras para la industria de la madera, fabricación, astilladores para la industria de la madera, fabricación, biseladoras para la industria de la madera, fabricación, cepilladoras para la industria de la madera, fabricación, compactadores para la industria de la madera, fabricación, desvenadoras para la industria de la madera, fabricación, enchapadoras para la industria de la madera, fabricación, engrapadoras para madera, fabricación, ensambladoras para la industria de la madera, fabricació	t	\N	\N
409	Fabricación de maquinaria y equipo para la industria del hule y del plástico	coextructoras para la industria del plástico, fabricación, compactadoras para la industria del plástico, fabricación, dosificadoras para la industria del plástico, fabricación, enfriadores para la industria del plástico, fabricación, estriadoras de llantas, fabricación, extructoras de plásticos, fabricación, extrusoras de hules, fabricación, granuladoras y peletizadoras de plásticos, fabricación, impresoras para la industria del plástico, fabricación, inyectoras de plásticos, fabricación, maquin	t	\N	\N
410	Fabricación de maquinaria y equipo para la industria alimentaria y de las bebidas	amasadoras para la industria alimentaria, fabricación, asadores para la industria alimentaria, fabricación, bandas enfriadoras para la industria alimentaria, fabricación, batidoras eléctricas para la industria alimentaria, fabricación, boleadoras para la industria alimentaria, fabricación, cafeteras de uso industrial, fabricación, cernedores para la industria alimentaria, fabricación, clasificadora y seleccionadora de productos alimenticios, fabricación, cortadoras para la industria alimenticia,	t	\N	\N
411	Fabricación de maquinaria y equipo para la industria textil	afelpadoras textiles, fabricación, bobinadoras textiles, fabricación, bordadoras textiles, fabricación, botonadoras, fabricación, calandras textiles, fabricación, cardadoras textiles, fabricación, cargadores de hilo, fabricación, centrifugas para tejido de punto, fabricación, compactadoras para tejido de punto, fabricación, compresoras textiles, fabricación, cortadoras para la industria textil, fabricación, desenrolladoras de telas, fabricación, deshilachadoras de textiles, fabricación, desmonta	t	\N	\N
412	Fabricación de maquinaria y equipo para la industria de la impresión	cajas tipo para impresoras, fabricación, compaginadoras, fabricación, cosedoras para imprenta, fabricación, filetes para impresión, fabricación, foliadoras, fabricación, galeras para impresión, fabricación, guías para impresoras, fabricación, guillotinas para imprenta, fabricación, imprentas, fabricación, lingotes para impresión, fabricación, maquinaria y equipo para la industria de la impresión, fabricación, piedras litográficas, fabricación, plegadoras para imprenta, fabricación, prensas para 	t	\N	\N
413	Fabricación de maquinaria y equipo para la industria del vidrio y otros minerales no metálicos	biseladoras para la industria del vidrio, fabricación, bloqueras para la industria del vidrio, fabricación, canteadoras para la industria del vidrio, fabricación, cortadoras para la industria del vidrio y otros minerales no metálicos, fabricación, discos de corte para la industria del vidrio y otros minerales no metálicos, fabricación, discos de pulido para la industria del vidrio, fabricación, hornos para cerámica, fabricación, hornos para la industria del cemento, fabricación, hornos para la i	t	\N	\N
414	Fabricación de maquinaria y equipo para otras industrias manufactureras	destiladores para laboratorio, fabricación, hornos para la industria química, fabricación, hornos para secado de madera, fabricación, maquinaria y equipo para aislar alambre y cable, fabricación, maquinaria y equipo para la industria automotriz, fabricación, maquinaria y equipo para la industria de la pintura, fabricación, maquinaria y equipo para la industria del calzado, fabricación, maquinaria y equipo para la industria del cartón, fabricación, maquinaria y equipo para la industria del corcho	t	\N	\N
415	Fabricación de aparatos fotográficos	ampliadores fotográficos, fabricación, bandejas para impresión y procesamiento fotográfico, fabricación, cámaras fotográficas digitales, fabricación, cámaras fotográficas, fabricación, cámaras proyectoras de películas, fabricación, depósitos para revelado, fabricación, equipo para edición de películas, fabricación, equipo y accesorios fotográficos, fabricación, exposímetros fotográficos, fabricación, flashes para cámaras fotográficas, fabricación, fotómetros fotográficos, fabricación, lavadoras 	t	\N	\N
416	Fabricación de máquinas fotocopiadoras	copiadoras, fabricación, duplicadoras, fabricación, fotocopiadoras, fabricación	t	\N	\N
417	Fabricación de otra maquinaria y equipo para el comercio y los servicios	aparatos ópticos de uso no oftálmico, fabricación, aspiradoras de uso industrial y comercial, fabricación, barredoras industriales y comerciales, fabricación, binoculares, fabricación, cajas registradoras, fabricación, calentadores industriales, fabricación, catalejos, fabricación, compactadores de desperdicios, fabricación, compactadores industriales de basura, fabricación, comparadores ópticos, fabricación, contadoras de monedas, fabricación, cotejadoras de hojas de papel, fabricación, equipo 	t	\N	\N
418	Fabricación de equipo de aire acondicionado y calefacción	absorbedores de polvo y vapor de uso industrial, fabricación, calderas de calefacción central, fabricación, calefactores de uso industrial y comercial, fabricación, calentadores de ambiente de uso industrial y comercial, fabricación, calentadores eléctricos para albercas, fabricación, compresores para sistemas para aire acondicionado, fabricación, depuradores de aire, fabricación, equipo de aire acondicionado excepto para vehículos de motor, fabricación, equipo de calefacción, fabricación, equip	t	\N	\N
419	Fabricación de equipo de refrigeración industrial y comercial	cámaras de refrigeración, fabricación, compresoras para refrigeración, fabricación, condensadores para cámaras frigoríficas, fabricación, congeladores para laboratorio, fabricación, equipo de refrigeración industrial y comercial, fabricación, equipo de refrigeración para equipo de transporte, fabricación, evaporadores para equipo de refrigeración, fabricación, exhibidores con refrigeración, fabricación, maquinaria y equipo para refrigeración industrial, fabricación, neveras industriales, fabrica	t	\N	\N
420	Fabricación de maquinaria y equipo para la industria metalmecánica	abrillantadoras de metales, fabricación, acanaladoras de metales, fabricación, afiladoras de metales, fabricación, aterrajadoras de metales, fabricación, avellanadores para trabajar metales, fabricación, biseladoras de metales, fabricación, brocas para metales, fabricación, bruñidoras de metales, fabricación, bulldozers para metalistería, fabricación, cepilladoras de metales, fabricación, centros de mecanizado, fabricación, contrataladros para metales, fabricación, cortadoras para la industria m	t	\N	\N
421	Fabricación de motores de combustión interna, turbinas y transmisiones	cadenas de transmisión para maquinaria industrial, fabricación, cadenas de transmisión, fabricación, cajas de transmisión de propulsión para maquinaria industrial, fabricación, cambiadores de velocidad para maquinaria industrial, fabricación, cojinetes planos para maquinaria industrial, fabricación, collares de transmisión de uso industrial, fabricación, embragues excepto para vehículos de motor, fabricación, engranajes de uso industrial, fabricación, generadores para turbinas, fabricación, gobe	t	\N	\N
422	Fabricación de bombas y sistemas de bombeo	aspersores de uso industrial, fabricación, bombas centrífugas, fabricación, bombas de medición de uso industrial, fabricación, bombas de potencia, fabricación, bombas de uso comercial, fabricación, bombas de uso doméstico, fabricación, bombas de uso industrial, fabricación, bombas de vacío, fabricación, bombas neumáticas de potencia, fabricación, bombas para bicicletas, fabricación, bombas para despachar y medir, fabricación, bombas para pozos petroleros, fabricación, cilindros de bomba de uso i	t	\N	\N
704	Almacenamiento de productos agrícolas que no requieren refrigeración	algodón, almacenamiento, granos, almacenamiento sin refrigeración, lana, almacenamiento sin refrigeración, productos agrícolas que no requieren refrigeración, almacenamiento, productos agrícolas, almacenamiento sin refrigeración, tabaco, almacenamiento sin refrigeración	t	\N	\N
423	Fabricación de maquinaria y equipo para levantar y trasladar	acarreadores de materiales, fabricación, andadores eléctricos de uso industrial, fabricación, andadores mecánicos para transporte de personas, fabricación, apiladores industriales, fabricación, bandas transportadoras, fabricación, cargadores de cinta, fabricación, cargadores de muelle para trasladar y levantar mercancías, fabricación, carros industriales para movimiento de carga, fabricación, carruseles para movimiento de carga, fabricación, contenedores para carga, fabricación, elevadores de ca	t	\N	\N
424	Fabricación de equipo para soldar y soldaduras	alambre para soldadura, fabricación, barras para soldaduras, fabricación, electrodos para soldadura eléctrica, fabricación, equipo de ultrasonido para soldadura, fabricación, equipo láser para soldadura, fabricación, equipo para soldar, fabricación, generadores de gas para soldadura, fabricación, materiales para soldadura, fabricación, soldadoras de resistencia eléctrica, fabricación	t	\N	\N
425	Fabricación de maquinaria y equipo para envasar y empacar	cerradoras de bolsas, fabricación, empacadoras industriales, fabricación, enlatadoras industriales, excepto para la industria alimentaria, fabricación, envolvedoras industriales, fabricación, equipo de calentamiento dieléctrico para empacar, fabricación, etiquetadoras industriales, fabricación, humectadores de etiquetas industriales, fabricación, llenadoras de bolsas, fabricación, maquinaria y equipo para tapar y sellar, fabricación	t	\N	\N
426	Fabricación de aparatos e instrumentos para pesar	balanzas de laboratorio, fabricación, balanzas de uso comercial, fabricación, balanzas de uso doméstico, fabricación, balanzas de uso industrial, fabricación, básculas de uso comercial, fabricación, básculas de uso doméstico, fabricación, básculas de uso industrial, fabricación, básculas de uso médico, fabricación, escalas de peso, fabricación, instrumentos para pesar, fabricación	t	\N	\N
427	Fabricación de otra maquinaria y equipo para la industria en general	activadores de potencia hidráulica, fabricación, activadores de potencia neumática, fabricación, caladoras de mano con motor, fabricación, centrífugas industriales, fabricación, cilindros de potencia hidráulica, fabricación, cinceles motorizados, fabricación, clavadoras de mano con motor, fabricación, destornilladores de mano con motor, fabricación, enfriadores de agua, fabricación, engrapadoras de mano con motor, fabricación, equipo para balanceo para la industria en general, fabricación, equip	t	\N	\N
428	Fabricación de computadoras y equipo periférico	adaptadores periféricos, fabricación, bocinas periféricas para computadora, fabricación, cajeros automáticos, fabricación, cámaras web, fabricación, computadoras analógicas, fabricación, computadoras centrales, fabricación, computadoras de mano (PDA), fabricación, computadoras digitales, fabricación, computadoras híbridas, fabricación, computadoras multiseat, fabricación, computadoras para escritorio, fabricación, computadoras personales, fabricación, computadoras portátiles, fabricación, comput	t	\N	\N
429	Fabricación de equipo telefónico	aparatos telefónicos, fabricación, auriculares, fabricación, centrales telefónicas, fabricación, conmutadores telefónicos, fabricación, contestadoras telefónicas, fabricación, equipo múltiplex para teléfono y telégrafo, fabricación, equipo telefónico, fabricación, faxes, fabricación, interruptores para equipo telefónico, fabricación, interruptores para equipo telegráfico, fabricación, protector electrónico de llamadas telefónicas, fabricación, retransmisoras de línea de comunicación, fabricación	t	\N	\N
430	Fabricación de equipo de transmisión y recepción de señales de radio y televisión, y equipo de comunicación inalámbrico	amplificadores para la transmisión y recepción de señales de radio y TV, fabricación, antenas de recepción, fabricación, antenas de transmisión y comunicación, fabricación, antenas para automóviles, fabricación, antenas para teléfonos celulares, fabricación, antenas para televisión, fabricación, antenas parabólicas, fabricación, antenas satelitales, fabricación, aparatos y equipos de comunicación de fibra óptica, fabricación, cámaras de televisión, fabricación, decodificadores de señal, fabricac	t	\N	\N
431	Fabricación de otros equipos de comunicación	alarmas antirrobos, fabricación, alarmas contra incendios, fabricación, alarmas para ambulancia, fabricación, alarmas para automóviles, fabricación, aparatos de control remoto infrarrojo y radio para la comunicación, fabricación, aparatos eléctricos de señalización, fabricación, detectores de fuego, fabricación, detectores de humo, fabricación, detectores de movimientos, fabricación, dispositivos eléctricos para señalamientos de tren, fabricación, equipo de control de tránsito peatonal, fabricac	t	\N	\N
432	Fabricación de equipo de audio y de video	altavoces, fabricación, autoestéreos, fabricación, bocinas para autoestéreos, fabricación, brazos de fonógrafo, fabricación, controles remotos para aparatos electrónicos de uso doméstico, fabricación, ecualizadores, fabricación, equipo de audio y video, fabricación, equipo de sonido, fabricación, estéreos, fabricación, fonógrafos, fabricación, grabadoras domésticas, fabricación, home cinemas, fabricación, mezcladoras de sonido, fabricación, micrófonos, fabricación, pantallas curvas de televisión	t	\N	\N
433	Fabricación de componentes electrónicos	agujas para fonógrafos, fabricación, amplificadores electrónicos, fabricación, arneses para uso electrónico, fabricación, atenuadores de señales, fabricación, bobinas de choque, fabricación, bobinas electrónicas, fabricación, bocinas (componente electrónico), fabricación, cabezas magnéticas, fabricación, capacitores electrónicos, fabricación, celdas de combustible en estado sólido, fabricación, celdas electroquímicas en estado sólido, fabricación, celdas fotoconductoras, fabricación, celdas foto	t	\N	\N
434	Fabricación de relojes	cerraduras de tiempo, fabricación, checadores de tiempo, fabricación, controles de tiempo, fabricación, cronómetros, fabricación, mecanismos para relojes, fabricación, minuteros, fabricación, partes para relojes, fabricación, programadores de tiempo, fabricación, relojes de agua, fabricación, relojes de arena, fabricación, relojes de bolsillo, fabricación, relojes de cuarzo, fabricación, relojes de pared, fabricación, relojes de péndulo, fabricación, relojes de pulsera, fabricación, relojes de s	t	\N	\N
435	Fabricación de otros instrumentos de medición, control, navegación, y equipo médico electrónico	acelerómetros, fabricación, actinómetros meteorológicos, fabricación, alcoholímetros, fabricación, altímetros aeronáuticos, fabricación, amperímetros, fabricación, analizadores coulométricos, fabricación, analizadores de absorción, fabricación, analizadores de distorsión, fabricación, analizadores de gas, fabricación, analizadores de humedad, fabricación, analizadores de impulsos, fabricación, analizadores de laboratorio, fabricación, analizadores de líquidos, fabricación, analizadores de proces	t	\N	\N
705	Otros servicios de almacenamiento con instalaciones especializadas	animales en pie, almacenamiento, automóviles sin rodar, almacenamiento, combustibles, almacenamiento, madera, almacenamiento, objetos sobredimensionados, almacenamiento, petróleo, almacenamiento	t	\N	\N
436	Fabricación y reproducción de medios magnéticos y ópticos	Blu-ray (BD), fabricación, CD cards, fabricación, cintas de audio vírgenes, fabricación, cintas de video en blanco, fabricación, cintas magnéticas pregrabadas, reproducción masiva, cintas magnéticas vírgenes, reproducción masiva, discos compactos (CD) pregrabados, reproducción masiva, discos compactos (CD) vírgenes, fabricación, discos de acetato vírgenes, fabricación, discos de acetato, reproducción masiva, discos de video digital (DVD) vírgenes, fabricación, discos de video digital (DVD), repr	t	\N	\N
437	Fabricación de focos	bombillas de gas, fabricación, bombillas de vidrio, fabricación, bombillas eléctricas, fabricación, bombillas para flash fotográfico, fabricación, bombillas para lámparas, fabricación, bombillas para linternas, fabricación, bombillas, fabricación, casquillos para focos, fabricación, casquillos para lámparas de iluminación, fabricación, filamentos, fabricación, focos ahorradores, fabricación, focos con carga de gas, fabricación, focos de proyección, fabricación, focos de xenón, fabricación, focos	t	\N	\N
438	Fabricación de lámparas ornamentales	candiles eléctricos, fabricación, lámparas arbotantes, fabricación, lámparas atrapa insectos, fabricación, lámparas colgantes, fabricación, lámparas de buró, fabricación, lámparas de emergencia, fabricación, lámparas de gas, fabricación, lámparas de gasolina, fabricación, lámparas de mano, fabricación, lámparas de mesa, fabricación, lámparas de pared, fabricación, lámparas de pedestal, fabricación, lámparas de pie, fabricación, lámparas de piso, fabricación, lámparas de techo, fabricación, lámpa	t	\N	\N
439	Fabricación de enseres electrodomésticos menores	abrelatas eléctricos de uso doméstico, fabricación, afiladores de cuchillos eléctricos de uso doméstico, fabricación, almohadas eléctricas, fabricación, aspiradoras de uso doméstico, fabricación, barredoras eléctricas de uso doméstico, fabricación, batidoras eléctricas de uso doméstico, fabricación, cafeteras de uso doméstico, fabricación, calentadores ambientales de uso doméstico, fabricación, calentadores eléctricos de uso doméstico, fabricación, carcasas para electrodomésticos menores, fabric	t	\N	\N
440	Fabricación de aparatos de línea blanca	aparatos de línea blanca, fabricación, calentadores de agua (boilers) de gas de uso doméstico, fabricación, calentadores de agua (boilers) de leña de uso doméstico, fabricación, calentadores solares, fabricación, campanas de cocina eléctricas de uso doméstico, fabricación, centros de lavado de uso doméstico, fabricación, compactadores de basura de uso doméstico, fabricación, congeladores de uso doméstico, fabricación, estufas de gas de uso doméstico, fabricación, estufas de petróleo, fabricación	t	\N	\N
441	Fabricación de motores y generadores eléctricos	anillos para motores y generadores eléctricos, fabricación, arrancadores para motor eléctrico, fabricación, arrancadores para motores industriales, fabricación, bobinas para motores y generadores eléctricos, fabricación, centros de control para motores eléctricos, fabricación, condensadores sincrónicos eléctricos, fabricación, contractores de motores industriales, fabricación, controladores de motores industriales, fabricación, controles para motores (relés de sobrecarga), fabricación, controles	t	\N	\N
442	Fabricación de equipo y aparatos de distribución de energía eléctrica	aislantes eléctricos de alta tensión, fabricación, alimentadores de voltaje, fabricación, apartarrayos, fabricación, arrancadores de estado sólido para transformador, fabricación, arrancadores de potencia eléctricos, fabricación, autotransformadores eléctricos, fabricación, autotransformadores para tableros de control, fabricación, balastros para control y distribución de energía eléctrica, fabricación, balastros para lámpara, fabricación, bobinas para equipo de control y distribución de energía	t	\N	\N
443	Fabricación de acumuladores y pilas	acumuladores automotrices, fabricación, acumuladores para automóviles, fabricación, acumuladores para camiones, fabricación, acumuladores para equipo agrícola, fabricación, acumuladores para equipo industrial, fabricación, acumuladores para ferrocarriles, fabricación, acumuladores para motocicletas, fabricación, acumuladores para uso industrial, fabricación, acumuladores solares, fabricación, acumuladores, fabricación, baterías automotrices, fabricación, baterías de almacenamiento de litio, fabr	t	\N	\N
444	Fabricación de cables de conducción eléctrica	alambre para comunicación, fabricación, alambre para conducción eléctrica, fabricación, alambre para instalaciones eléctricas, fabricación, cables coaxiales, fabricación, cables de conducción eléctrica, fabricación, cables de fibra de vidrio, fabricación, cables eléctricos, fabricación, cables aislantes forrados de asbesto, fabricación, cables multiconductores, fabricación, cables multifiliales, fabricación, cables multipolares, fabricación, cables para arneses, fabricación, cables para comunica	t	\N	\N
445	Fabricación de enchufes, contactos, fusibles y otros accesorios para instalaciones eléctricas	abrazaderas de tierra (dispositivos de cableado eléctrico), fabricación, apagadores eléctricos, fabricación, cajas de conexión para instalaciones eléctricas, fabricación, cajas para instalaciones eléctricas, fabricación, canales protectores para instalaciones eléctricas, fabricación, clavijas para cableado eléctrico, fabricación, conectores y terminales para instalaciones eléctricas, fabricación, conmutadores para instalaciones eléctricas, fabricación, contactos eléctricos, fabricación, cortacir	t	\N	\N
446	Fabricación de productos eléctricos de carbón y grafito	anillos de carbón y grafito, fabricación, ánodos eléctricos de carbón, fabricación, barras de carbón y grafito para uso industrial, fabricación, barras eléctricas de carbón, fabricación, carbones eléctricos para lámparas de arco, fabricación, carbones eléctricos para pilas, fabricación, carbones para contactos eléctricos, fabricación, electrodos de carbón, fabricación, electrodos de grafito, fabricación, electrodos para uso térmico, fabricación, escobillas de carbón y grafito, fabricación, molde	t	\N	\N
447	Fabricación de otros productos eléctricos	aceleradores de partículas, fabricación, aceleradores lineales, fabricación, capacitores eléctricos, fabricación, cargadores para celular, fabricación, chicharras, fabricación, condensadores eléctricos, fabricación, cordones eléctricos con conectores (extensiones eléctricas), fabricación, dispositivos eléctricos para abrir y cerrar puertas, fabricación, eliminadores de corriente eléctrica, fabricación, equipo para electrolineras, fabricación, equipo para estaciones de recarga de vehículos eléctr	t	\N	\N
448	Fabricación de automóviles y camionetas	ambulancias, fabricación, automóviles de 4 cilindros, fabricación, automóviles de 6 cilindros, fabricación, automóviles de 8 cilindros, fabricación, automóviles eléctricos, fabricación, automóviles híbridos, fabricación, automóviles no tripulados y vehículos robóticos, fabricación, automóviles, fabricación, camiones ligeros de reparto, fabricación, camionetas de carga ligera, fabricación, carrozas fúnebres, fabricación, chasis de camiones ligeros, fabricación, chasis para automóvil, fabricación,	t	\N	\N
449	Fabricación de camiones y tractocamiones	autobuses foráneos, fabricación, autobuses integrales, fabricación, autobuses suburbanos, fabricación, autobuses urbanos, fabricación, autobuses, fabricación, camiones de bomberos, fabricación, camiones de carga, fabricación, camiones de pasajeros, fabricación, camiones de volteo, fabricación, camiones grúa, fabricación, camiones híbridos, fabricación, camiones para propósitos especiales, fabricación, camiones para recolección de basura, fabricación, camiones plataforma, fabricación, camiones ta	t	\N	\N
450	Fabricación de carrocerías y remolques	cajas de camiones, fabricación , cajas de volteo, fabricación, cajas low-boy, fabricación, cajas refrigeradas, fabricación, cajas secas, fabricación, cajas tipo van, fabricación, campers, fabricación, carrocería de camión grúa, fabricación, carrocerías cerveceras, fabricación, carrocerías de aluminio, fabricación, carrocerías de caja abierta, fabricación, carrocerías de caja cerrada, fabricación, carrocerías de madera, fabricación, carrocerías de tolva, fabricación, carrocerías de volteo, fabric	t	\N	\N
451	Fabricación de motores y sus partes para vehículos automotrices	agujas de inyector para motores automotrices, fabricación, anillos para motores automotrices, fabricación, árbol de levas para motores automotrices, fabricación, arcos de pistón para motores automotrices, fabricación, balancines para motores automotrices, fabricación, bielas para motores automotrices, fabricación, bloques para motores automotrices, fabricación, bombas de aceite para motores automotrices, fabricación, bombas de gasolina para motores automotrices, fabricación, bulones para motores	t	\N	\N
452	Fabricación de equipo eléctrico y electrónico y sus partes para vehículos automotores	alternadores para vehículos, automotores; fabricación, arneses eléctricos para vehículos automotores, fabricación, bieletas para sistemas de dirección para vehículos automotores, fabricación, bocinas de claxon para vehículos automotores, fabricación, bombas de encendido para motores de vehículos automotores, fabricación, bujías para vehículos automotores, fabricación, cableados para vehículos automotores, fabricación, cables para bujías para vehículos automotores, fabricación, centralitas electr	t	\N	\N
453	Fabricación de partes de sistemas de dirección y de suspensión para vehículos automotrices	amortiguadores para vehículos automotrices, fabricación, ballestas para sistemas de dirección, fabricación, barras de torsión para vehículos automotrices, fabricación, barras estabilizadora para sistemas de dirección de vehículos automotrices, fabricación, bases de amortiguadores para vehículos automotrices, fabricación, brazos de suspensión para vehículos automotrices, fabricación, cajas de dirección estándar para vehículos automotrices, fabricación, cajas de dirección hidráulica para vehículos	t	\N	\N
454	Fabricación de partes de sistemas de frenos para vehículos automotrices	balatas para frenos automotrices, fabricación, bombas para frenos automotrices, fabricación, bostear para frenos automotrices, fabricación, chicotes para frenos automotrices, fabricación, cilindros maestros para frenos automotrices, fabricación, cilindros para frenos automotrices, fabricación, diafragmas para frenos automotrices, fabricación, discos y campanas para frenos automotrices, fabricación, frenos ABS para vehículos automotrices, fabricación, frenos automotrices, fabricación, frenos de a	t	\N	\N
455	Fabricación de partes de sistemas de transmisión para vehículos automotores	árbol de transmisión para vehículos automotores, fabricación, cajas de cambios para sistemas de transmisión, fabricación, calabazos de hierro para sistemas de transmisión, fabricación, chumaceras para sistemas de transmisión de vehículos automotores, fabricación, clutch, fabricación, collarines para sistemas de transmisión, fabricación, convertidores de torque para sistemas de transmisión de vehículos automotores, fabricación, crucetas para sistemas de transmisión de vehículos automotores, fabri	t	\N	\N
456	Fabricación de asientos y accesorios interiores para vehículos automotores	accesorios textiles para interiores de vehículos automotores, fabricación, alfombras para vehículos automotores, fabricación, asientos para autobuses, fabricación, asientos para automóviles, fabricación, asientos para aviones, fabricación, asientos para camiones, fabricación, asientos para motocicleta, fabricación, asientos para vehículos automotores, fabricación, bolsas de aire para vehículos automotrices, fabricación, cinturones de seguridad para vehículos automotores, fabricación, cubiertas p	t	\N	\N
457	Fabricación de piezas metálicas troqueladas para vehículos automotrices	capós metálicos troquelados para vehículos automotrices, fabricación, cofres troquelados para vehículos automotrices, fabricación, cubrefaros metálicos troquelados para vehículos automotrices, fabricación, defensas metálicas troqueladas para vehículos automotrices, fabricación, estribos metálicos troquelados para vehículos automotrices, fabricación, guardapolvos metálicos troquelados para vehículos automotrices, fabricación, lienzos metálicos troquelados para vehículos automotrices, fabricación,	t	\N	\N
458	Fabricación de otras partes para vehículos automotrices	canastillas para vehículos automotrices, fabricación, capotas para vehículos automotrices, fabricación, convertidores catalíticos para vehículos automotrices, fabricación, cornetas para vehículos automotrices, fabricación, elevadores de cristales para vehículos automotrices, fabricación, enfriadores de aceite para vehículos automotrices, fabricación, escapes para vehículos automotrices, fabricación, espejos para vehículos automotrices, fabricación, filtros de aceite para vehículos automotrices, 	t	\N	\N
459	Fabricación de equipo aeroespacial	aeronaves, fabricación, aeronaves, reconstrucción, aeroplanos, fabricación, alas de aeronaves, fabricación, aviones de tripulación remota (drones), fabricación, avionetas, fabricación, avionetas, reconstrucción, bombas de motor para aeronaves, fabricación, cámaras de combustión para aeronaves, fabricación, cápsulas espaciales, fabricación, cohetes espaciales, fabricación, dirigibles aeroespaciales, fabricación, equipo aeroespacial, fabricación, equipo aeroespacial, reconstrucción, estabilizadore	t	\N	\N
460	Fabricación de equipo ferroviario	agujas de cambio para vías de ferrocarril, fabricación, anclas para riel, fabricación, árbol de cambio para vías de ferrocarril, fabricación, candados para vías de ferrocarril, fabricación, carros de ferrocarril, fabricación, carros dormitorio para ferrocarriles, fabricación, equipo ferroviario, fabricación, equipo ferroviario, reconstrucción, frenos de ferrocarril, fabricación, furgones para ferrocarril, fabricación, góndolas para carga de transporte ferroviario, fabricación, locomotoras de fer	t	\N	\N
461	Fabricación de embarcaciones	balsas salvavidas, fabricación, barcazas, fabricación, barcos de remolque, fabricación, barcos para pesca, fabricación, barcos plataforma, fabricación, barcos recreativos, fabricación y conversión, barcos recreativos, fabricación y reparación, barcos recreativos, fabricación, reparación y conversión, barcos, fabricación, botes inflables de casco rígido, fabricación, botes para transporte de carga, fabricación, botes para transporte de pasajeros, fabricación, botes salvavidas, fabricación, buques	t	\N	\N
466	Fabricación de muebles, excepto cocinas integrales, muebles modulares de baño y muebles de oficina y estantería	antecomedores, fabricación, armarios, fabricación, asientos para bebé para colocarse en automóviles, fabricación, bancas (excepto de concreto), fabricación, bancas para iglesias, fabricación, bancos para pedicura, fabricación, bases para cama, fabricación, biombos, fabricación, burós, fabricación, butacas, fabricación, cabeceras para cama, fabricación, camas de hospital, fabricación, camastros de madera, fabricación, camillas, fabricación, centros de entretenimiento (muebles), fabricación, clóse	t	\N	\N
467	Fabricación de muebles de oficina y estantería	aparadores, fabricación, archiveros de madera, fabricación, archiveros de metal, fabricación, archiveros de plástico, fabricación, casilleros, fabricación, credenzas, fabricación, escritorios de madera, fabricación, escritorios de metal, fabricación, escritorios, fabricación, estantería, fabricación, casilleros (lockers), fabricación, mamparas de metal, fabricación, muebles de oficina y estantería, ensamblado en serie, muebles de oficina, ensamblado en serie, muebles de oficina, fabricación, mue	t	\N	\N
468	Fabricación de colchones	box spring, fabricación, colchones de agua, fabricación, colchones de borra, fabricación, colchones de hule espuma, fabricación, colchones de resorte, fabricación	t	\N	\N
469	Fabricación de persianas y cortineros	accesorios para cortineros, fabricación, accesorios para persianas, fabricación, cortineros de madera, fabricación, cortineros de metal, fabricación, cortineros de plástico, fabricación, cortineros, fabricación, persianas de aluminio, fabricación, persianas de bambú, fabricación, persianas de madera, fabricación, persianas de PVC, fabricación, persianas deslizantes, fabricación, persianas enrollables, fabricación, persianas horizontales, fabricación, persianas plegables, fabricación, persianas p	t	\N	\N
470	Fabricación de equipo no electrónico para uso médico, dental y para laboratorio	abrazaderas ortopédicas, fabricación, aleaciones para amalgamas dentales, fabricación, alicates dentales, fabricación, andaderas ortopédicas, fabricación, aparatos ortopédicos, fabricación, aparatos y equipo no electrónicos para laboratorio, fabricación, aspiradoras de uso médico, fabricación, atomizadores médicos, fabricación, autoclaves de uso médico no electrónicos, fabricación, bastones ortopédicos, fabricación, baumanómetros, fabricación, bisturíes no desechables, fabricación, bombas neumát	t	\N	\N
471	Fabricación de material desechable de uso médico	abatelenguas, fabricación, agujas hipodérmicas, fabricación, agujas para sutura, fabricación, algodón absorbente de uso médico, fabricación, apósitos, fabricación, batas desechables, fabricación, bisturíes desechables, fabricación, bolsas recolectoras de orina, fabricación, bolsas recolectoras de sangre, fabricación, botas desechables, fabricación, calzado desechable, fabricación, cánulas quirúrgicas, fabricación, catéteres, fabricación, cemento para hueso, fabricación, cemento quirúrgico, fabri	t	\N	\N
472	Fabricación de artículos oftálmicos	anteojos, fabricación, armazones de uso oftálmico, fabricación, calipers y reglas de uso oftálmico, fabricación, choppers, fabricación, cristales oftálmicos, fabricación, espátulas de uso oftálmico, fabricación, gemelos, fabricación, goggles, fabricación, instrumentos oftálmicos, fabricación, lentes bifocales, fabricación, lentes de contacto, fabricación, lentes de plástico, fabricación, lentes de uso oftálmico, fabricación, lentes intraoculares, fabricación, lentes monofocales, fabricación, len	t	\N	\N
473	Acuñación e impresión de monedas	billetes de banco, impresión, monedas de metales no preciosos, acuñación, monedas de metales preciosos, acuñación, papel moneda, impresión	t	\N	\N
474	Orfebrería y joyería de metales y piedras preciosos	anillos de metales preciosos, fabricación, aretes de metales preciosos, fabricación, argollas de oro, fabricación, argollas de plata, fabricación, artículos religiosos de metales preciosos, fabricación, bolsos de mano de metales preciosos, fabricación, brazaletes de metales preciosos, fabricación, cadenas de metales preciosos, fabricación, charolas de metales preciosos, fabricación, collares de metales preciosos, fabricación, correas para reloj de metales preciosos, fabricación, cuchillería de m	t	\N	\N
475	Joyería de metales y piedras no preciosos y de otros materiales	anillos de metales no preciosos, fabricación, aretes de bisutería, fabricación, aretes de metales no preciosos, fabricación, brazaletes de bisutería, fabricación, brazaletes de metales no preciosos, fabricación, cadenas de bisutería, fabricación, cadenas de metales no preciosos, fabricación, collares de bisutería, fabricación, collares de metales no preciosos, fabricación, dijes de metales no preciosos, fabricación, gargantillas de metales no preciosos, fabricación, joyería con chapa de oro, fab	t	\N	\N
476	Metalistería de metales no preciosos	artículos ornamentales de metales no preciosos, fabricación, charolas de agradecimiento, fabricación, figuras ornamentales de metales no preciosos, fabricación, floreros de metales no preciosos, fabricación, jarrones de metales no preciosos, fabricación, platones de metales no preciosos, fabricación, reconocimientos de metales no preciosos, fabricación, trofeos de metales no preciosos, fabricación	t	\N	\N
477	Fabricación de artículos deportivos	aletas para buceo, fabricación, anzuelos para pesca, fabricación, aparatos para ejercicio, fabricación, aparejos para pesca, fabricación, balones para basquetbol, fabricación, balones para futbol americano, fabricación, balones para futbol soccer, fabricación, balones para voleibol, fabricación, barras aeróbicas para gimnasio, fabricación, barras para gimnasio, fabricación, bases para béisbol, fabricación, biceps curl, fabricación, bicicletas para ejercicio, fabricación, bolas de billar, fabrica	t	\N	\N
478	Fabricación de juguetes	accesorios para muñecas, fabricación, alcancías, fabricación, andaderas para bebé, fabricación, autos de juguete, fabricación, avalanchas, fabricación, aviones de juguete, fabricación, baleros de juguete, fabricación, bloques para juego, fabricación, caballitos mecedores, fabricación, camiones de juguete, fabricación, campanas de juguete, fabricación, carriolas para para bebé, fabricación, carros de pedales para niños, fabricación, dados de juguete, fabricación, dardos, fabricación, dominós, fab	t	\N	\N
479	Fabricación de artículos y accesorios para escritura, pintura, dibujo y actividades de oficina	accesorios para dibujo, fabricación, accesorios para pintura artística, fabricación, aceite de nogal para pintura artística, fabricación, acuarelas, fabricación, afilaminas (equipo para dibujo), fabricación, arcilla para modelar, fabricación, artículos de oficina no electrónicos, fabricación, artículos para pintura artística, fabricación, bolígrafos, fabricación, borradores para pizarrón, fabricación, brochas de mano para pintura artística, fabricación, broches para hojas de papel, fabricación, 	t	\N	\N
732	Operadores de servicios de telecomunicaciones vía satélite	estaciones terrestres para operadores de comunicaciones satelitales, servicios de, operadores de servicios de telecomunicaciones vía satélite, reventa de servicios de telecomunicaciones por satélite, telecomunicaciones por satélite	t	\N	\N
480	Fabricación de anuncios y señalamientos	anuncios bipolares, fabricación, anuncios de acero inoxidable, fabricación, anuncios de aluminio, fabricación, anuncios de latón, fabricación, anuncios de neón, fabricación, anuncios de unicel, fabricación, anuncios electrónicos, fabricación, anuncios en impresión digital, fabricación, anuncios espectaculares, fabricación, anuncios giratorios de viento, fabricación, anuncios luminosos, fabricación, anuncios moldeados en acrílico, fabricación, anuncios publicitarios, fabricación, anuncios rotativ	t	\N	\N
481	Fabricación de instrumentos musicales	acordeones, fabricación, armónicas, fabricación, arpas, fabricación, autófonos, fabricación, bajos eléctricos (instrumento musical), fabricación, bajos electroacústicos (instrumento musical), fabricación, bambú (instrumento musical), fabricación, bandurria de madera, fabricación, banjos, fabricación, baterías, fabricación, bombos, fabricación, bongós, fabricación, bugles, fabricación, cabazas, fabricación, cajas musicales, fabricación, caliopes, fabricación, campanas musicales, fabricación, cari	t	\N	\N
482	Fabricación de cierres, botones y agujas	agujas para coser a mano, fabricación, agujas para coser a máquina, fabricación, alfileres, fabricación, botones de madera para la industria textil, fabricación, botones de metal para la industria textil, fabricación, botones de plástico para la industria textil, fabricación, botones de poliéster para la industria textil, fabricación, botones, fabricación, broches de presión, fabricación, broches para prendas de vestir, fabricación, cierres para productos textiles, fabricación, cremalleras para 	t	\N	\N
483	Fabricación de escobas, cepillos y similares	brochas para barniz, fabricación, brochas para el afeitado, fabricación, brochas para pintura no artística, fabricación, cepillos de uso doméstico, fabricación, cepillos dentales excepto eléctricos, fabricación, cepillos industriales, fabricación, cepillos lavaplatos, fabricación, cepillos para aspiradoras, fabricación, escobas de mijo, fabricación, escobas de plástico, fabricación, escobas industriales, fabricación, escobas manuales, fabricación, escobetas, fabricación, escobetillas de plástico	t	\N	\N
484	Fabricación de velas y veladoras	cirios, fabricación, parafinas (velas), fabricación, veladoras, fabricación, velas aromáticas, fabricación, velas decorativas, fabricación, velas, fabricación, velitas para pastel, fabricación, velitas para posada, fabricación	t	\N	\N
485	Fabricación de ataúdes	ataúdes de fibra de vidrio, fabricación, ataúdes de madera, fabricación, ataúdes de metal, fabricación, ataúdes metálicos, fabricación, ataúdes, fabricación	t	\N	\N
486	Otras industrias manufactureras	adornos de navidad de diversos materiales, fabricación, árboles artificiales, fabricación, árboles de navidad artificiales, fabricación, arreglos florales artificiales, fabricación, artesanías a base de conchas, fabricación, artesanías de hojas de elote, elaboración, artesanías de plastilina epóxica, fabricación, artículos para novia como tocados y ramos, fabricación, bastones excepto ortopédicos, fabricación, boquillas para fumar, fabricación, césped artificial, fabricación, cigarrillos electró	t	\N	\N
487	Comercio al por mayor de abarrotes	abarrotes, comercio al por mayor en tiendas de abarrotes, bodegas, distribuidoras y oficinas de ventas a través de métodos tradicionales o por internet, aceites comestibles, comercio al por mayor en tiendas de abarrotes, bodegas, distribuidoras y oficinas de ventas a través de métodos tradicionales o por internet, aderezos envasados, comercio al por mayor en tiendas de abarrotes, bodegas, distribuidoras y oficinas de ventas a través de métodos tradicionales o por internet, agua purificada envasa	t	\N	\N
488	Comercio al por mayor de carnes rojas	carne de borrego, comercio al por mayor especializado a través de métodos tradicionales o por internet, carne de bovino, comercio al por mayor especializado a través de métodos tradicionales o por internet, carne de caprino, comercio al por mayor especializado a través de métodos tradicionales o por internet, carne de cerdo, comercio al por mayor especializado a través de métodos tradicionales o por internet, carne de chivo, comercio al por mayor especializado a través de métodos tradicionales o	t	\N	\N
489	Comercio al por mayor de carne de aves	carne de aves, comercio al por mayor en bodegas, distribuidoras y oficinas de ventas a través de métodos tradicionales o por internet, carne de aves, comercio al por mayor especializado a través de métodos tradicionales o por internet, carne de avestruz, comercio al por mayor especializado a través de métodos tradicionales o por internet, carne de codorniz, comercio al por mayor especializado a través de métodos tradicionales o por internet, carne de ganso, comercio al por mayor especializado a 	t	\N	\N
490	Comercio al por mayor de pescados y mariscos	almejas congeladas, comercio al por mayor especializado a través de métodos tradicionales o por internet, almejas frescas, comercio al por mayor especializado a través de métodos tradicionales o por internet, bacalao congelado, comercio al por mayor especializado a través de métodos tradicionales o por internet, bacalao fresco, comercio al por mayor especializado a través de métodos tradicionales o por internet, bacalao salado, comercio al por mayor especializado a través de métodos tradicionale	t	\N	\N
491	Comercio al por mayor de frutas y verduras frescas	acelgas frescas, comercio al por mayor especializado a través de métodos tradicionales o por internet, aguacates frescos, comercio al por mayor especializado a través de métodos tradicionales o por internet, ajos frescos, comercio al por mayor especializado a través de métodos tradicionales o por internet, almendras, comercio al por mayor especializado a través de métodos tradicionales o por internet en tiendas de frutas y verduras frescas, apios frescos, comercio al por mayor especializado a tr	t	\N	\N
492	Comercio al por mayor de huevo	huevo de aves, comercio al por mayor especializado a través de métodos tradicionales o por internet, huevo de avestruz, comercio al por mayor especializado a través de métodos tradicionales o por internet, huevo de codorniz, comercio al por mayor especializado a través de métodos tradicionales o por internet, huevo de faisán, comercio al por mayor especializado a través de métodos tradicionales o por internet, huevo de gallina, comercio al por mayor especializado a través de métodos tradicionale	t	\N	\N
493	Comercio al por mayor de semillas y granos alimenticios, especias y chiles secos	achiote (especia), comercio al por mayor especializado a través de métodos tradicionales o por internet, ajonjolí (semilla), comercio al por mayor especializado a través de métodos tradicionales o por internet en tiendas de semillas y granos alimenticios, especias y chiles secos, ajos deshidratados (especia), comercio al por mayor especializado a través de métodos tradicionales o por internet, albahaca (especia), comercio al por mayor especializado a través de métodos tradicionales o por interne	t	\N	\N
924	Consultorios del sector público de audiología y de terapia ocupacional, física y del lenguaje	audiología en consultorios del sector público, terapia del lenguaje en consultorios del sector público, terapia deportiva en consultorios del sector público, terapia física en consultorios del sector público, terapia ocupacional en consultorios del sector público	t	\N	\N
494	Comercio al por mayor de leche y otros productos lácteos	bebidas lácteas fermentadas a base de lactobacilos, comercio al por mayor especializado a través de métodos tradicionales o por internet, crema ácida, comercio al por mayor especializado a través de métodos tradicionales o por internet, crema de leche, comercio al por mayor especializado a través de métodos tradicionales o por internet, crema dulce, comercio al por mayor especializado a través de métodos tradicionales o por internet, crema natural, comercio al por mayor especializado a través de	t	\N	\N
495	Comercio al por mayor de embutidos	carnes adobadas, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, carnes adobadas, comercio al por mayor especializado a través de métodos tradicionales o por internet, carnes ahumadas, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, carnes ahumadas, comercio al por mayor especializado a través de métodos tradicionales o por internet, carnes deshidratadas	t	\N	\N
496	Comercio al por mayor de dulces y materias primas para repostería	abrillantadores para repostería, comercio al por mayor especializado a través de métodos tradicionales o por internet, aceite de coco, comercio al por mayor especializado a través de métodos tradicionales o por internet, acido cítrico, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua de azahar, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua de rosas, comercio al por mayor especializado a través de métodos tradi	t	\N	\N
497	Comercio al por mayor de pan y pasteles	baguettes, comercio al por mayor especializado a través de métodos tradicionales o por internet, bizcochos, comercio al por mayor especializado a través de métodos tradicionales o por internet, bolillos y teleras, comercio al por mayor especializado a través de métodos tradicionales o por internet, bollos, comercio al por mayor especializado a través de métodos tradicionales o por internet, donas, comercio al por mayor especializado a través de métodos tradicionales o por internet, galletas dulc	t	\N	\N
498	Comercio al por mayor de botanas y frituras	botanas, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, botanas, comercio al por mayor especializado a través de métodos tradicionales o por internet en tiendas de botanas, cacahuates (botana), comercio al por mayor especializado a través de métodos tradicionales o por internet, cacahuates enchilados (botana), comercio al por mayor especializado a través de métodos tradicionales o por internet, cacahuates fritos (botana), c	t	\N	\N
499	Comercio al por mayor de conservas alimenticias	alimentos conservados en aceite, comercio al por mayor especializado a través de métodos tradicionales o por internet, alimentos conservados en almíbar, comercio al por mayor especializado a través de métodos tradicionales o por internet, alimentos conservados por el proceso de congelación, comercio al por mayor especializado a través de métodos tradicionales o por internet, alimentos conservados por el proceso de deshidratación, comercio al por mayor especializado a través de métodos tradiciona	t	\N	\N
500	Comercio al por mayor de miel	cera de abejas, comercio al por mayor especializado a través de métodos tradicionales o por internet, derivados de la miel, comercio al por mayor especializado a través de métodos tradicionales o por internet, jalea real, comercio al por mayor especializado a través de métodos tradicionales o por internet, jarabe de maíz, comercio al por mayor especializado a través de métodos tradicionales o por internet, jarabe de maple, comercio al por mayor especializado a través de métodos tradicionales o p	t	\N	\N
501	Comercio al por mayor de otros alimentos	aceite comestible, comercio al por mayor especializado a través de métodos tradicionales o por internet, azúcar, comercio al por mayor especializado a través de métodos tradicionales o por internet, budines, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, budines, comercio al por mayor especializado a través de métodos tradicionales o por internet, café en grano, comercio al por mayor especializado a través de métodos tradic	t	\N	\N
502	Comercio al por mayor de bebidas no alcohólicas y hielo	agua embotellada purificada, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua envasada con saborizante, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua envasada saborizada, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua envasada sin saborizante, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua mineral envasada, comercio al por 	t	\N	\N
503	Comercio al por mayor de vinos y licores	aguardiente envasado, comercio al por mayor especializado a través de métodos tradicionales o por internet, anís (bebida alcohólica) envasado, comercio al por mayor especializado a través de métodos tradicionales o por internet, bebidas destiladas envasadas, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, bebidas destiladas envasadas, comercio al por mayor especializado a través de métodos tradicionales o por internet, brand	t	\N	\N
504	Comercio al por mayor de cerveza	barril de cerveza, comercio al por mayor especializado a través de métodos tradicionales o por internet, caguamas envasadas (cervezas), comercio al por mayor especializado a través de métodos tradicionales o por internet, cervecerías (bodegas, distribuidoras y oficinas de ventas), comercio al por mayor especializado a través de métodos tradicionales o por internet en, cerveza ale envasada, comercio al por mayor especializado a través de métodos tradicionales o por internet, cerveza amarga envasa	t	\N	\N
505	Comercio al por mayor de cigarros, puros y tabaco	boquillas para cigarros, comercio al por mayor especializado a través de métodos tradicionales o por internet, boquillas para pipas, comercio al por mayor especializado a través de métodos tradicionales o por internet, ceniceros para puros, comercio al por mayor especializado a través de métodos tradicionales o por internet, cigarreras (excepto de metales preciosos), comercio al por mayor especializado a través de métodos tradicionales o por internet, cigarrillos, comercio al por mayor especiali	t	\N	\N
506	Comercio al por mayor de fibras, hilos y telas	algodón en paca, comercio al por mayor especializado a través de métodos tradicionales o por internet, algodón en pluma, comercio al por mayor especializado a través de métodos tradicionales o por internet, alpaca (tela), comercio al por mayor especializado a través de métodos tradicionales o por internet, borras de fibras textiles, comercio al por mayor especializado a través de métodos tradicionales o por internet, brocado (tela), comercio al por mayor especializado a través de métodos tradici	t	\N	\N
953	Asilos y otras residencias del sector privado para el cuidado de ancianos	asilos del sector privado para el cuidado de ancianos, servicios de, casas del sector privado de retiro para ancianos, servicios de, residencias de descanso del sector privado para ancianos sin cuidados de enfermeras, servicios de	t	\N	\N
507	Comercio al por mayor de blancos	almohadas nuevas, comercio al por mayor especializado a través de métodos tradicionales o por internet, blancos artesanales, comercio al por mayor especializado a través de métodos tradicionales o por internet, blancos nuevos bordados, comercio al por mayor especializado a través de métodos tradicionales o por internet, blancos nuevos deshilados, comercio al por mayor especializado a través de métodos tradicionales o por internet, blancos nuevos para bebé, comercio al por mayor especializado a t	t	\N	\N
508	Comercio al por mayor de cueros y pieles	charol, comercio al por mayor especializado a través de métodos tradicionales o por internet, colorantes para el teñido de cueros, comercio al por mayor especializado a través de métodos tradicionales o por internet, cueros cocidos, comercio al por mayor especializado a través de métodos tradicionales o por internet, cueros con curtido vegetal, comercio al por mayor especializado a través de métodos tradicionales o por internet, cueros crudos, comercio al por mayor especializado a través de méto	t	\N	\N
509	Comercio al por mayor de otros productos textiles	abrazaderas (pasamanería), comercio al por mayor especializado a través de métodos tradicionales o por internet, agujas para coser, comercio al por mayor especializado a través de métodos tradicionales o por internet, agujas para tejer, comercio al por mayor especializado a través de métodos tradicionales o por internet, alfileres, comercio al por mayor especializado a través de métodos tradicionales o por internet, artículos de mercería, comercio al por mayor especializado a través de métodos t	t	\N	\N
510	Comercio al por mayor de ropa, bisutería y accesorios de vestir	abanicos nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, abrigos nuevos para bebé, comercio al por mayor especializado a través de métodos tradicionales o por internet, abrigos nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, accesorios de vestir artesanales nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, accesorios de vestir nuevos de cuero, piel y materiales 	t	\N	\N
511	Comercio al por mayor de calzado	accesorios nuevos para calzado, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, accesorios nuevos para calzado, comercio al por mayor especializado a través de métodos tradicionales o por internet, agujetas nuevas para calzado, comercio al por mayor especializado a través de métodos tradicionales o por internet, alpargatas nuevas, comercio al por mayor especializado a través de métodos tradicionales o por internet, botas nue	t	\N	\N
512	Comercio al por mayor de productos farmacéuticos	agua oxigenada para consumo humano, comercio al por mayor especializado a través de métodos tradicionales o por internet, agujas para jeringas para consumo humano, comercio al por mayor especializado a través de métodos tradicionales o por internet, alcohol de botiquín, comercio al por mayor especializado a través de métodos tradicionales o por internet, alcohol etílico para consumo humano, comercio al por mayor especializado a través de métodos tradicionales o por internet, algodón para curació	t	\N	\N
513	Comercio al por mayor de artículos de perfumería y cosméticos	aceite para bebé, comercio al por mayor especializado a través de métodos tradicionales o por internet, aceite para cabello, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua de colonia, comercio al por mayor especializado a través de métodos tradicionales o por internet, agua de lavanda, comercio al por mayor especializado a través de métodos tradicionales o por internet, artículos de belleza, comercio al por mayor a través de métodos tradicionales o por	t	\N	\N
514	Comercio al por mayor de artículos de joyería y relojes	anillos (joyería) nuevos de metales preciosos, comercio al por mayor especializado a través de métodos tradicionales o por internet, aretes nuevos de metales preciosos, comercio al por mayor especializado a través de métodos tradicionales o por internet, brazaletes nuevos de metales preciosos, comercio al por mayor especializado a través de métodos tradicionales o por internet, broches (joyería) nuevos de metales preciosos, comercio al por mayor especializado a través de métodos tradicionales o 	t	\N	\N
515	Comercio al por mayor de grabaciones de audio y video en medios físicos	cartuchos de audio nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, cartuchos de cinta magnética para audio y video, comercio al por mayor especializado a través de métodos tradicionales o por internet, cartuchos de video nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, cartuchos nuevos de videojuegos, comercio al por mayor especializado a través de métodos tradicionales o por internet, cartuchos sin grabar	t	\N	\N
516	Comercio al por mayor de juguetes y bicicletas	accesorios nuevos para consolas de video, comercio al por mayor especializado a través de métodos tradicionales o por internet, aeronaves nuevas de juguete, comercio al por mayor especializado a través de métodos tradicionales o por internet, alcancías nuevas de juguete, comercio al por mayor especializado a través de métodos tradicionales o por internet, animales nuevos de juguete, comercio al por mayor especializado a través de métodos tradicionales o por internet, aros nuevos de juguete, come	t	\N	\N
517	Comercio al por mayor de artículos y aparatos deportivos	aletas de natación nuevas, comercio al por mayor especializado a través de métodos tradicionales o por internet, anzuelos nuevos para pesca deportiva, comercio al por mayor especializado a través de métodos tradicionales o por internet, aparatos nuevos para gimnasio, comercio al por mayor especializado a través de métodos tradicionales o por internet, armas de fuego nuevas para deporte y caza, comercio al por mayor especializado a través de métodos tradicionales o por internet, artículos y apara	t	\N	\N
518	Comercio al por mayor de artículos de papelería	ábacos, comercio al por mayor especializado a través de métodos tradicionales o por internet, acetatos, comercio al por mayor especializado a través de métodos tradicionales o por internet, acuarelas, comercio al por mayor especializado a través de métodos tradicionales o por internet, agendas y calendarios (artículos de papelería), comercio al por mayor especializado a través de métodos tradicionales o por internet, arillos para engargolar, comercio al por mayor especializado a través de método	t	\N	\N
519	Comercio al por mayor de libros	atlas nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, audiodiscos nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, audiolibros nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, diccionarios nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, enciclopedias nuevas, comercio al por mayor especializado a través de métodos tra	t	\N	\N
520	Comercio al por mayor de revistas y periódicos	comics nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, fotonovelas nuevas, comercio al por mayor especializado a través de métodos tradicionales o por internet, historietas nuevas, comercio al por mayor especializado a través de métodos tradicionales o por internet, periódicos (excepto para reciclaje), comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, periódicos (excepto para recic	t	\N	\N
521	Comercio al por mayor de electrodomésticos menores y aparatos de línea blanca	aparatos de aire acondicionado domésticos nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, aparatos de calefacción domésticos nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, aparatos de línea blanca nuevos, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, aparatos de línea blanca nuevos, comercio al por mayor especializado a través de m	t	\N	\N
522	Comercio al por mayor de fertilizantes, plaguicidas y semillas para siembra	abonos de origen orgánico, comercio al por mayor especializado a través de métodos tradicionales o por internet, abonos en barritas, comercio al por mayor especializado a través de métodos tradicionales o por internet, abonos en pastillas, comercio al por mayor especializado a través de métodos tradicionales o por internet, abonos foliares, comercio al por mayor especializado a través de métodos tradicionales o por internet, abonos granulados, comercio al por mayor especializado a través de méto	t	\N	\N
523	Comercio al por mayor de medicamentos veterinarios y alimentos para animales, excepto mascotas	acaricidas para animales (excepto para mascotas), comercio al por mayor especializado a través de métodos tradicionales o por internet, alfalfa forrajera, comercio al por mayor especializado a través de métodos tradicionales o por internet, alimentos balanceados para animales (excepto para mascotas), comercio al por mayor especializado a través de métodos tradicionales o por internet, alimentos balanceados para animales acuáticos (excepto mascotas de ornato), comercio al por mayor especializado 	t	\N	\N
524	Comercio al por mayor de cemento, tabique y grava	accesorios para baño, comercio al por mayor especializado a través de métodos tradicionales o por internet, adhesivos para pisos y recubrimientos cerámicos, comercio al por mayor especializado a través de métodos tradicionales o por internet, adocretos, comercio al por mayor especializado a través de métodos tradicionales o por internet, adoquines, comercio al por mayor especializado a través de métodos tradicionales o por internet, aglutinantes para la construcción, comercio al por mayor especi	t	\N	\N
525	Comercio al por mayor de otros materiales para la construcción, excepto de madera y metálicos	aislantes térmicos de espuma celulósica, comercio al por mayor especializado a través de métodos tradicionales o por internet, aislantes térmicos de espuma de poliestireno, comercio al por mayor especializado a través de métodos tradicionales o por internet, aislantes térmicos de espuma de polietileno, comercio al por mayor especializado a través de métodos tradicionales o por internet, aislantes térmicos de espuma de poliuretano, comercio al por mayor especializado a través de métodos tradicion	t	\N	\N
526	Comercio al por mayor de materiales metálicos para la construcción y la manufactura	alambre recocido, comercio al por mayor especializado a través de métodos tradicionales o por internet, alambres de acero, comercio al por mayor especializado a través de métodos tradicionales o por internet, alambres de cobre, comercio al por mayor especializado a través de métodos tradicionales o por internet, alambres de hilo de cobre esmaltado, comercio al por mayor especializado a través de métodos tradicionales o por internet, alambres de púas, comercio al por mayor especializado a través 	t	\N	\N
527	Comercio al por mayor de productos químicos para la industria farmacéutica y para otro uso industrial	abrasivos, comercio al por mayor especializado a través de métodos tradicionales o por internet, aceites (químicos), comercio al por mayor especializado a través de métodos tradicionales o por internet, aceites de almendra, comercio al por mayor especializado a través de métodos tradicionales o por internet, aceites de limón, comercio al por mayor especializado a través de métodos tradicionales o por internet, aceites de naranja, comercio al por mayor especializado a través de métodos tradiciona	t	\N	\N
528	Comercio al por mayor de envases en general, papel y cartón para la industria	accesorios para el flejado, comercio al por mayor especializado a través de métodos tradicionales o por internet, accesorios para embalaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, acondicionadores (embalaje) nuevos para la industria, comercio al por mayor especializado a través de métodos tradicionales o por internet, acumuladores de frío nuevos para embalaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, acumu	t	\N	\N
529	Comercio al por mayor de madera para la construcción y la industria	aglomerados de madera para la construcción y la industria, comercio al por mayor especializado a través de métodos tradicionales o por internet, apliques de madera para la construcción y la industria, comercio al por mayor especializado a través de métodos tradicionales o por internet, barrotes de madera para la construcción y la industria, comercio al por mayor especializado a través de métodos tradicionales o por internet, celosías de madera para la construcción y la industria, comercio al por	t	\N	\N
530	Comercio al por mayor de equipo y material eléctrico	acumuladores de electricidad, comercio al por mayor especializado a través de métodos tradicionales o por internet, adaptadores eléctricos, comercio al por mayor especializado a través de métodos tradicionales o por internet, aisladores, comercio al por mayor especializado a través de métodos tradicionales o por internet, aislantes eléctricos, comercio al por mayor especializado a través de métodos tradicionales o por internet, alambres de magneto, comercio al por mayor especializado a través de	t	\N	\N
531	Comercio al por mayor de pintura	accesorios (no artísticos) para pintar muebles e inmuebles, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, accesorios (no artísticos) para pintar muebles e inmuebles, comercio al por mayor especializado a través de métodos tradicionales o por internet, acetona en bodegas, distribuidoras y oficinas de venta de pinturas, comercio al por mayor especializado a través de métodos tradicionales o por internet, aguarrás en bodegas,	t	\N	\N
532	Comercio al por mayor de vidrios y espejos	bloques de vidrio (vidrio blocks), comercio al por mayor especializado a través de métodos tradicionales o por internet, cristales (excepto para automóviles, camionetas y camiones), comercio al por mayor especializado a través de métodos tradicionales o por internet, cristales antibalas, comercio al por mayor especializado a través de métodos tradicionales o por internet, cristales antirreflejantes, comercio al por mayor especializado a través de métodos tradicionales o por internet, cristales b	t	\N	\N
533	Comercio al por mayor de ganado y aves en pie	aves de corral en pie, comercio al por mayor especializado a través de métodos tradicionales o por internet, aves en pie, comercio al por mayor especializado a través de métodos tradicionales o por internet, avestruces en pie, comercio al por mayor especializado a través de métodos tradicionales o por internet, becerros en pie, comercio al por mayor especializado a través de métodos tradicionales o por internet, bovinos en pie, comercio al por mayor especializado a través de métodos tradicionale	t	\N	\N
534	Comercio al por mayor de otras materias primas para otras industrias	abrazaderas, comercio al por mayor especializado a través de métodos tradicionales o por internet, aldabas, comercio al por mayor especializado a través de métodos tradicionales o por internet, anclas para cortinas, comercio al por mayor especializado a través de métodos tradicionales o por internet, armellas, comercio al por mayor especializado a través de métodos tradicionales o por internet, bandas para uso industrial, comercio al por mayor especializado a través de métodos tradicionales o po	t	\N	\N
535	Comercio al por mayor de combustibles	aceites lubricantes de uso automotriz, comercio al por mayor especializado a través de métodos tradicionales o por internet, aceites lubricantes para vehículos de motor, comercio al por mayor especializado a través de métodos tradicionales o por internet, aceites, grasas lubricantes, aditivos y anticongelantes para vehículos de motor, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, aditivos de uso automotriz, comercio al por	t	\N	\N
536	Comercio al por mayor de artículos desechables	bolsas de plástico (excepto para basura), comercio al por mayor especializado a través de métodos tradicionales o por internet, charolas desechables, comercio al por mayor especializado a través de métodos tradicionales o por internet, cubiertos desechables, comercio al por mayor especializado a través de métodos tradicionales o por internet, moldes desechables, comercio al por mayor especializado a través de métodos tradicionales o por internet, platos desechables, comercio al por mayor especia	t	\N	\N
537	Comercio al por mayor de desechos metálicos	chatarra electrónica o basura tecnológica, comercio al por mayor especializado a través de métodos tradicionales o por internet, chatarra metálica para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de acero inoxidable para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de aluminio para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por interne	t	\N	\N
538	Comercio al por mayor de desechos de papel y de cartón	cartón usado limpio sin clasificar para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, cartón usado limpio y clasificado para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, cartón usado sucio para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de archivo muerto para reciclaje, comercio al por mayor especializado a través de métodos tradici	t	\N	\N
539	Comercio al por mayor de desechos de vidrio	botellas usadas de vidrio para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de vidrio para reciclaje (excepto de la demolición), comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de vidrio para reciclaje, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, envases usados de vidrio para reciclaje, comercio al por mayor especi	t	\N	\N
540	Comercio al por mayor de desechos de plástico	bolsas usadas de plástico para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, botellas usadas de plástico para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, cajas usadas de plástico para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de plástico para reciclaje (excepto de la demolición), comercio al por mayor especializado a través de mét	t	\N	\N
541	Comercio al por mayor de otros materiales de desecho	desechos de cuero y piel para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de fibras textiles para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de hule para reciclaje, comercio al por mayor especializado a través de métodos tradicionales o por internet, desechos de madera de la construcción para reciclaje, comercio al por mayor especializado a través de métodos tradicionales 	t	\N	\N
542	Comercio al por mayor de maquinaria y equipo agropecuario, forestal y para la pesca	abrevaderos, comercio al por mayor especializado a través de métodos tradicionales o por internet, accesorios para gallos de pelea, comercio al por mayor especializado a través de métodos tradicionales o por internet, aereadores para la acuicultura, comercio al por mayor especializado a través de métodos tradicionales o por internet, almartigones para caballos, comercio al por mayor especializado a través de métodos tradicionales o por internet, anillos nasales para ganado, comercio al por mayor	t	\N	\N
543	Comercio al por mayor de maquinaria y equipo para la construcción y la minería	acanaladoras para la construcción, comercio al por mayor especializado a través de métodos tradicionales o por internet, alimentadoras para la minería, comercio al por mayor especializado a través de métodos tradicionales o por internet, allanadoras, comercio al por mayor especializado a través de métodos tradicionales o por internet, andamios para cimbra, comercio al por mayor especializado a través de métodos tradicionales o por internet, andamios para la construcción, comercio al por mayor es	t	\N	\N
544	Comercio al por mayor de maquinaria y equipo para la industria manufacturera	Comercio al por mayor de maquinaria y equipo para la industria manufacturera	t	\N	\N
545	Comercio al por mayor de equipo de telecomunicaciones, fotografía y cinematografía	accesorios para laboratorios de fotoacabado, comercio al por mayor especializado a través de métodos tradicionales o por internet, alarmas de seguridad electrónica, comercio al por mayor especializado a través de métodos tradicionales o por internet, altavoces, comercio al por mayor especializado a través de métodos tradicionales o por internet, amplificadores, comercio al por mayor especializado a través de métodos tradicionales o por internet, antenas de radiotransmisión o radiorecepción, come	t	\N	\N
546	Comercio al por mayor de artículos y accesorios para diseño y pintura artística	acuarelas (pinturas de agua) para pintura artística, comercio al por mayor especializado a través de métodos tradicionales o por internet, aerógrafos, comercio al por mayor especializado a través de métodos tradicionales o por internet, artículos para serigrafía, comercio al por mayor especializado a través de métodos tradicionales o por internet, artículos y accesorios para arquitectura, comercio al por mayor en bodegas, distribuidoras y oficinas de ventas, artículos y accesorios para arquitect	t	\N	\N
547	Comercio al por mayor de mobiliario, equipo e instrumental médico y de laboratorio	agujas de sutura, comercio al por mayor especializado a través de métodos tradicionales o por internet, agujas hipodérmicas, comercio al por mayor especializado a través de métodos tradicionales o por internet, amalgamadores, comercio al por mayor especializado a través de métodos tradicionales o por internet, anestesia dental, comercio al por mayor especializado a través de métodos tradicionales o por internet, aparatos de electrocirugía, comercio al por mayor especializado a través de métodos 	t	\N	\N
548	Comercio al por mayor de maquinaria y equipo para otros servicios y para actividades comerciales	anaqueles comerciales, comercio al por mayor especializado a través de métodos tradicionales o por internet, asadores comerciales, comercio al por mayor especializado a través de métodos tradicionales o por internet, balanzas y básculas para pesar alimentos, comercio al por mayor especializado a través de métodos tradicionales o por internet, barras comerciales para alimentos, comercio al por mayor especializado a través de métodos tradicionales o por internet, básculas cuenta piezas para alimen	t	\N	\N
549	Comercio al por mayor de mobiliario, equipo, y accesorios de cómputo	accesorios de cómputo nuevos, comercio al por mayor a través de métodos tradicionales o por internet en bodegas, distribuidoras y oficinas de ventas, accesorios de cómputo nuevos, comercio al por mayor especializado a través de métodos tradicionales o por internet, accesorios nuevos para computadora, comercio al por mayor especializado a través de métodos tradicionales o por internet, baterías para computadoras portátiles, comercio al por mayor especializado a través de métodos tradicionales o p	t	\N	\N
550	Comercio al por mayor de mobiliario y equipo de oficina	accesorios para copiadora, comercio al por mayor especializado a través de métodos tradicionales o por internet, agendas electrónicas para oficina, comercio al por mayor especializado a través de métodos tradicionales o por internet, archiveros para oficina, comercio al por mayor especializado a través de métodos tradicionales o por internet, armarios para oficina, comercio al por mayor especializado a través de métodos tradicionales o por internet, básculas cuenta piezas para dinero, comercio a	t	\N	\N
551	Comercio al por mayor de otra maquinaria y equipo de uso general	andamios de uso general, comercio al por mayor especializado a través de métodos tradicionales o por internet, aparejos de uso general, comercio al por mayor especializado a través de métodos tradicionales o por internet, baleros y retenes de uso general, comercio al por mayor especializado a través de métodos tradicionales o por internet, batas de uso industrial, comercio al por mayor especializado a través de métodos tradicionales o por internet, bombas industriales de uso general, comercio al	t	\N	\N
552	Comercio al por mayor de camiones	autobuses foráneos nuevos y usados, comercio al por mayor especializado a través de métodos tradicionales o por internet, autobuses nuevos y usados de pasajeros, comercio al por mayor especializado a través de métodos tradicionales o por internet, autobuses nuevos y usados, comercio al por mayor especializado a través de métodos tradicionales o por internet, autobuses urbanos nuevos y usados, comercio al por mayor especializado a través de métodos tradicionales o por internet, cajas de carga nue	t	\N	\N
553	Comercio al por mayor de partes y refacciones nuevas para automóviles, camionetas y camiones	acumuladores nuevos para automóviles, camionetas y camiones, comercio al por mayor especializado a través de métodos tradicionales o por internet, alarmas nuevas para automóviles, camionetas y camiones, comercio al por mayor especializado a través de métodos tradicionales o por internet, alfombras nuevas para automóviles, camionetas y camiones, comercio al por mayor especializado a través de métodos tradicionales o por internet, alternadores nuevos para automóviles, camionetas y camiones, comerc	t	\N	\N
554	Intermediación de comercio al por mayor de productos agropecuarios	intermediación entre negocios en la compra o venta de productos agropecuarios a través de métodos tradicionales, intermediación entre negocios en la compra o venta de productos agropecuarios por internet, subasta entre negocios de productos agropecuarios nuevos o usados a través de métodos tradicionales, subasta entre negocios de productos agropecuarios nuevos o usados por internet	t	\N	\N
555	Intermediación de comercio al por mayor de productos para la industria, el comercio y los servicios	intermediación entre negocios en la compra o venta de productos para el comercio a través de métodos tradicionales, intermediación entre negocios en la compra o venta de productos para el comercio por internet, intermediación entre negocios en la compra o venta de productos para la industria a través de métodos tradicionales, intermediación entre negocios en la compra o venta de productos para la industria por internet, intermediación entre negocios en la compra o venta de productos para los ser	t	\N	\N
556	Intermediación de comercio al por mayor de productos de uso doméstico y personal	distribución de vales de compra, intermediación entre negocios en la compra o venta de productos de uso doméstico a través de métodos tradicionales, intermediación entre negocios en la compra o venta de productos de uso doméstico por internet, intermediación entre negocios en la compra o venta de productos de uso personal a través de métodos tradicionales, intermediación entre negocios en la compra o venta de productos de uso personal por internet, subasta entre negocios de productos nuevos o us	t	\N	\N
557	Comercio al por menor en tiendas de abarrotes, ultramarinos y misceláneas	abarrotes, comercio al por menor en tiendas de abarrotes, ultramarinos y misceláneas a través de métodos tradicionales o por internet, aceites comestibles, comercio al por menor en tiendas de abarrotes, ultramarinos y misceláneas a través de métodos tradicionales o por internet, aderezos envasados, comercio al por menor en tiendas de abarrotes, ultramarinos y misceláneas a través de métodos tradicionales o por internet, agua purificada envasada, comercio al por menor en tiendas de abarrotes, ult	t	\N	\N
558	Comercio al por menor de carnes rojas	carne de borrego, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de bovino, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de caprino, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de cerdo, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de chivo, comercio al por menor especializado a través de métodos tradicionales o	t	\N	\N
559	Comercio al por menor de carne de aves	carne de aves, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de avestruz, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de codorniz, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de ganso, comercio al por menor especializado a través de métodos tradicionales o por internet, carne de guajolote, comercio al por menor especializado a través de métodos tradicional	t	\N	\N
560	Comercio al por menor de pescados y mariscos	almejas congeladas, comercio al por menor especializado a través de métodos tradicionales o por internet, almejas frescas, comercio al por menor especializado a través de métodos tradicionales o por internet, bacalao congelado, comercio al por menor especializado a través de métodos tradicionales o por internet, bacalao fresco, comercio al por menor especializado a través de métodos tradicionales o por internet, bacalao salado, comercio al por menor especializado a través de métodos tradicionale	t	\N	\N
561	Comercio al por menor de frutas y verduras frescas	acelgas frescas, comercio al por menor especializado a través de métodos tradicionales o por internet, aguacates frescos, comercio al por menor especializado a través de métodos tradicionales o por internet, ajos frescos, comercio al por menor especializado a través de métodos tradicionales o por internet, almendras, comercio al por menor especializado a través de métodos tradicionales o por internet en tiendas de frutas y verduras frescas, apios frescos, comercio al por menor especializado a tr	t	\N	\N
562	Comercio al por menor de semillas y granos alimenticios, especias y chiles secos	achiote (especia), comercio al por menor especializado a través de métodos tradicionales o por internet, ajonjolí (semilla), comercio al por menor especializado a través de métodos tradicionales o por internet, ajos deshidratados (especia), comercio al por menor especializado a través de métodos tradicionales o por internet, albahaca (especia), comercio al por menor especializado a través de métodos tradicionales o por internet, almendras, comercio al por menor especializado a través de métodos 	t	\N	\N
563	Comercio al por menor de leche, otros productos lácteos y embutidos	bebidas lácteas fermentadas a base de lactobacilos, comercio al por menor especializado a través de métodos tradicionales o por internet, carnes adobadas, comercio al por menor especializado a través de métodos tradicionales o por internet, carnes ahumadas, comercio al por menor especializado a través de métodos tradicionales o por internet, carnes deshidratadas, comercio al por menor especializado a través de métodos tradicionales o por internet, carnes frías, comercio al por menor especializad	t	\N	\N
564	Comercio al por menor de dulces y materias primas para repostería	abrillantadores para repostería, comercio al por menor especializado a través de métodos tradicionales o por internet, aceite de coco, comercio al por menor especializado a través de métodos tradicionales o por internet, acido cítrico, comercio al por menor especializado a través de métodos tradicionales o por internet, agua de azahar, comercio al por menor especializado a través de métodos tradicionales o por internet, agua de rosas, comercio al por menor especializado a través de métodos tradi	t	\N	\N
565	Comercio al por menor de paletas de hielo y helados	helados, comercio al por menor especializado a través de métodos tradicionales o por internet, neverías (tiendas), comercio al por menor especializado a través de métodos tradicionales o por internet en, nieves, comercio al por menor especializado a través de métodos tradicionales o por internet, paletas de hielo, comercio al por menor especializado a través de métodos tradicionales o por internet, paleterías (tiendas), comercio al por menor especializado a través de métodos tradicionales o por 	t	\N	\N
566	Comercio al por menor de otros alimentos	aceite comestible, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos conservados en aceite, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos conservados en almíbar, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos conservados por el proceso de congelación, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos conserv	t	\N	\N
567	Comercio al por menor de vinos y licores	aguardiente envasado, comercio al por menor especializado a través de métodos tradicionales o por internet, anís (bebida alcohólica) envasado, comercio al por menor especializado a través de métodos tradicionales o por internet, bebidas destiladas envasadas, comercio al por menor especializado a través de métodos tradicionales o por internet, brandi (brandy) envasado, comercio al por menor especializado a través de métodos tradicionales o por internet, champaña (champagne) envasada, comercio al 	t	\N	\N
568	Comercio al por menor de cerveza	barril de cerveza, comercio al por menor especializado a través de métodos tradicionales o por internet, caguamas envasadas (cervezas), comercio al por menor especializado a través de métodos tradicionales o por internet, cervecerías (tiendas), comercio al por menor especializado a través de métodos tradicionales o por internet en, cerveza ale envasada, comercio al por menor especializado a través de métodos tradicionales o por internet, cerveza amarga envasada, comercio al por menor especializa	t	\N	\N
569	Comercio al por menor de bebidas no alcohólicas y hielo	agua embotellada purificada, comercio al por menor especializado a través de métodos tradicionales o por internet, agua envasada con saborizante, comercio al por menor especializado a través de métodos tradicionales o por internet, agua envasada saborizada, comercio al por menor especializado a través de métodos tradicionales o por internet, agua envasada sin saborizante, comercio al por menor especializado a través de métodos tradicionales o por internet, agua mineral envasada, comercio al por 	t	\N	\N
570	Comercio al por menor de cigarros, puros y tabaco	boquillas para cigarros, comercio al por menor especializado a través de métodos tradicionales o por internet, boquillas para pipas, comercio al por menor especializado a través de métodos tradicionales o por internet, ceniceros para puros, comercio al por menor especializado a través de métodos tradicionales o por internet, cigarreras (excepto de metales preciosos), comercio al por menor especializado a través de métodos tradicionales o por internet, cigarrillos, comercio al por menor especiali	t	\N	\N
571	Comercio al por menor en supermercados	abarrotes, comercio al por menor a través de métodos tradicionales o por internet en supermercados, accesorios de cómputo, comercio al por menor a través de métodos tradicionales o por internet en supermercados, agua envasada, comercio al por menor a través de métodos tradicionales o por internet en supermercados, alimentos congelados, comercio al por menor a través de métodos tradicionales o por internet en supermercados, alimentos frescos, comercio al por menor a través de métodos tradicionale	t	\N	\N
572	Comercio al por menor en minisupers	abarrotes, comercio al por menor a través de métodos tradicionales o por internet en minisupers, agua envasada, comercio al por menor a través de métodos tradicionales o por internet en minisupers, alimentos congelados, comercio al por menor a través de métodos tradicionales o por internet en minisupers, alimentos frescos, comercio al por menor a través de métodos tradicionales o por internet en minisupers, alimentos, comercio al por menor a través de métodos tradicionales o por internet en mini	t	\N	\N
573	Comercio al por menor en tiendas departamentales	accesorios de cómputo, comercio al por menor a través de métodos tradicionales o por internet en tiendas departamentales, aparatos de línea blanca, comercio al por menor a través de métodos tradicionales o por internet en tiendas departamentales, aparatos electrónicos, comercio al por menor a través de métodos tradicionales o por internet en tiendas departamentales, artículos artesanales para el hogar, comercio al por menor a través de métodos tradicionales o por internet en tiendas departamenta	t	\N	\N
574	Comercio al por menor de telas	alpaca (tela), comercio al por menor especializado a través de métodos tradicionales o por internet, borras de fibras textiles, comercio al por menor especializado a través de métodos tradicionales o por internet, brocado (tela), comercio al por menor especializado a través de métodos tradicionales o por internet, casimir, comercio al por menor especializado a través de métodos tradicionales o por internet, chenille, comercio al por menor especializado a través de métodos tradicionales o por int	t	\N	\N
575	Comercio al por menor de blancos	almohadas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, blancos artesanales, comercio al por menor especializado a través de métodos tradicionales o por internet, blancos nuevos bordados, comercio al por menor especializado a través de métodos tradicionales o por internet, blancos nuevos deshilados, comercio al por menor especializado a través de métodos tradicionales o por internet, blancos nuevos para bebé, comercio al por menor especializado a t	t	\N	\N
576	Comercio al por menor de artículos de mercería y bonetería	abrazaderas (pasamanería), comercio al por menor especializado a través de métodos tradicionales o por internet, agujas para coser, comercio al por menor especializado a través de métodos tradicionales o por internet, agujas para tejer, comercio al por menor especializado a través de métodos tradicionales o por internet, alfileres, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos de bonetería, comercio al por menor especializado a través de métodos 	t	\N	\N
577	Comercio al por menor de ropa, excepto de bebé y lencería	abrigos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, batas de baño nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, batas escolares de laboratorio nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, bermudas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, bikinis (trajes de baño) nuevos, comercio al por menor especia	t	\N	\N
578	Comercio al por menor de ropa de bebé	abrigos nuevos para bebé, comercio al por menor especializado a través de métodos tradicionales o por internet, baberos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, batas nuevas para bebé, comercio al por menor especializado a través de métodos tradicionales o por internet, boutiques de ropa nueva para bebé, comercio al por menor especializado a través de métodos tradicionales o por internet en, calcetines nuevos para bebé, comercio al por menor e	t	\N	\N
579	Comercio al por menor de lencería	baby dolls nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, batas de dormir nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, bikinis (pantaletas) nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, boutiques de lencería nueva, comercio al por menor especializado a través de métodos tradicionales o por internet en, boxers nuevos para dama, comercio al por menor espec	t	\N	\N
580	Comercio al por menor de disfraces, trajes típicos y vestidos de novia	batas nuevas para chef, comercio al por menor especializado a través de métodos tradicionales o por internet, boutiques de disfraces nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet en, boutiques de ropa de bautizo nueva, comercio al por menor especializado a través de métodos tradicionales o por internet en, boutiques de ropa de novia nueva, comercio al por menor especializado a través de métodos tradicionales o por internet en, boutiques de ropa de p	t	\N	\N
581	Comercio al por menor de bisutería y accesorios de vestir	abanicos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios de vestir artesanales nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios de vestir nuevos (excepto de cuero, piel y materiales sucedáneos), comercio al por menor especializado a través de métodos tradicionales o por internet, adornos nuevos para el cabello (bisutería), comercio al por menor especializado a través de métodos tradic	t	\N	\N
582	Comercio al por menor de ropa de cuero y piel y de otros artículos de estos materiales	artículos de talabartería, comercio al por menor especializado a través de métodos tradicionales o por internet, bolsos de mano nuevos de cuero, piel y materiales sucedáneos, comercio al por menor especializado a través de métodos tradicionales o por internet, boutiques de ropa nueva de cuero, piel y materiales sucedáneos, comercio al por menor especializado a través de métodos tradicionales o por internet en, carpetas nuevas de cuero, piel y materiales sucedáneos, comercio al por menor especial	t	\N	\N
583	Comercio al por menor de pañales desechables	pañales desechables para adultos, comercio al por menor especializado a través de métodos tradicionales o por internet, pañales desechables para niños, comercio al por menor especializado a través de métodos tradicionales o por internet, pañales desechables, comercio al por menor especializado a través de métodos tradicionales o por internet, toallas sanitarias, comercio al por menor especializado a través de métodos tradicionales o por internet	t	\N	\N
584	Comercio al por menor de sombreros	sombrererías, comercio al por menor especializado a través de métodos tradicionales o por internet en, sombreros artesanales nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, sombreros de paja, comercio al por menor especializado a través de métodos tradicionales o por internet, sombreros nuevos de cuero, comercio al por menor especializado a través de métodos tradicionales o por internet, sombreros nuevos de fibras duras, comercio al por menor especia	t	\N	\N
585	Comercio al por menor de calzado	accesorios nuevos para calzado, comercio al por menor especializado a través de métodos tradicionales o por internet, agujetas nuevas para calzado, comercio al por menor especializado a través de métodos tradicionales o por internet, alpargatas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, botas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, botines nuevos, comercio al por menor especializado a través 	t	\N	\N
954	Asilos y otras residencias del sector público para el cuidado de ancianos	asilos del sector público para el cuidado de ancianos, servicios de, casas del sector público de retiro para ancianos, servicios de, residencias de descanso del sector público para ancianos sin cuidados de enfermeras, servicios de	t	\N	\N
587	Farmacias con minisúper	abarrotes, comercio al por menor a través de métodos tradicionales o por internet en farmacias con minisúper, aceites comestibles, comercio al por menor a través de métodos tradicionales o por internet en farmacias con minisúper, aderezos envasados, comercio al por menor a través de métodos tradicionales o por internet en farmacias con minisúper, agua oxigenada, comercio al por menor a través de métodos tradicionales o por internet en farmacias con minisúper, agua purificada envasada, comercio a	t	\N	\N
588	Comercio al por menor de productos naturistas, medicamentos homeopáticos y de complementos alimenticios	alimentos naturistas a base de soya, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos naturistas, comercio al por menor especializado a través de métodos tradicionales o por internet, boticas homeopáticas, comercio al por menor especializado a través de métodos tradicionales o por internet en, complementos alimenticios para consumo humano, comercio al por menor especializado a través de métodos tradicionales o por internet, cosméticos faciales natur	t	\N	\N
589	Comercio al por menor de lentes	accesorios oftálmicos, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios para lentes, comercio al por menor especializado a través de métodos tradicionales o por internet, anteojos (armazón y lente) bifocales, comercio al por menor especializado a través de métodos tradicionales o por internet, anteojos (armazón y lente) monofocales, comercio al por menor especializado a través de métodos tradicionales o por internet, anteojos (armazón y lente) para	t	\N	\N
590	Comercio al por menor de artículos ortopédicos	andadores ortopédicos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, aparatos nuevos para sordera, comercio al por menor especializado a través de métodos tradicionales o por internet, aparatos ortopédicos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos ortopédicos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, asientos ortopédicos nuevos para baño	t	\N	\N
591	Comercio al por menor de artículos de perfumería y cosméticos	aceite para bebé, comercio al por menor especializado a través de métodos tradicionales o por internet, aceite para el cabello, comercio al por menor especializado a través de métodos tradicionales o por internet, agua de colonia, comercio al por menor especializado a través de métodos tradicionales o por internet, agua de lavanda, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos de belleza, comercio al por menor especializado a través de métodos tr	t	\N	\N
592	Comercio al por menor de artículos de joyería y relojes	adornos nuevos de metales preciosos, comercio al por menor especializado a través de métodos tradicionales o por internet, anillos (joyería) nuevos de metales preciosos, comercio al por menor especializado a través de métodos tradicionales o por internet, aretes nuevos de metales preciosos, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos decorativos nuevos de metales preciosos, comercio al por menor especializado a través de métodos tradicionales o	t	\N	\N
593	Comercio al por menor de grabaciones de audio y video en medios físicos	cartuchos de audio nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, cartuchos de cinta magnética para audio y video, comercio al por menor especializado a través de métodos tradicionales o por internet, cartuchos de video nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, cartuchos nuevos de videojuegos, comercio al por menor especializado a través de métodos tradicionales o por internet, cartuchos sin grabar	t	\N	\N
594	Comercio al por menor de juguetes	accesorios nuevos para consolas de video, comercio al por menor especializado a través de métodos tradicionales o por internet, aeronaves nuevas de juguete, comercio al por menor especializado a través de métodos tradicionales o por internet, alcancías nuevas de juguete, comercio al por menor especializado a través de métodos tradicionales o por internet, animales nuevos de juguete, comercio al por menor especializado a través de métodos tradicionales o por internet, aros nuevos de juguete, come	t	\N	\N
595	Comercio al por menor de bicicletas y triciclos	agencias de bicicletas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet en, asientos nuevos para bicicletas y triciclos, comercio al por menor especializado a través de métodos tradicionales o por internet, bicicletas cross nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, bicicletas de turismo nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, bicicletas deportivas 	t	\N	\N
596	Comercio al por menor de equipo y material fotográfico	accesorios nuevos de equipo fotográfico, comercio al por menor especializado a través de métodos tradicionales o por internet, baterías para cámaras fotográficas, comercio al por menor especializado a través de métodos tradicionales o por internet, cables nuevos mini USB para cámaras fotográficas digitales, comercio al por menor especializado a través de métodos tradicionales o por internet, cámaras fotográficas APS (Advanced Photo System) nuevas, comercio al por menor especializado a través de 	t	\N	\N
597	Comercio al por menor de artículos y aparatos deportivos	alas delta nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, aletas de natación nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, almartigones nuevos para caballos, comercio al por menor especializado a través de métodos tradicionales o por internet, anzuelos nuevos para pesca deportiva, comercio al por menor especializado a través de métodos tradicionales o por internet, aparatos nuevos para gimnasio, comerc	t	\N	\N
598	Comercio al por menor de instrumentos musicales	acordeones nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, amplificadores de audio nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, armónicas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, arpas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, atriles nuevos, comercio al por menor especializado a través de métodos t	t	\N	\N
599	Comercio al por menor de artículos de papelería	ábacos, comercio al por menor especializado a través de métodos tradicionales o por internet, acetatos, comercio al por menor especializado a través de métodos tradicionales o por internet, acuarelas, comercio al por menor especializado a través de métodos tradicionales o por internet, agendas y calendarios (artículos de papelería), comercio al por menor especializado a través de métodos tradicionales o por internet, arillos para engargolar, comercio al por menor especializado a través de método	t	\N	\N
600	Comercio al por menor de libros	atlas nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, audiodiscos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, audiolibros nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, diccionarios nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, enciclopedias nuevas, comercio al por menor especializado a través de métodos tra	t	\N	\N
601	Comercio al por menor de revistas y periódicos	comics nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, fotonovelas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, historietas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, periódicos de circulación nacional, comercio al por menor especializado a través de métodos tradicionales o por internet, periódicos de circulación regional o estatal, comercio al por men	t	\N	\N
602	Comercio al por menor de mascotas y sus accesorios	acaricidas para mascotas, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios para mascotas, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos balanceados para mascotas, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos concentrados para mascotas, comercio al por menor especializado a través de métodos tradicionales o por internet, alimentos enlatados para masc	t	\N	\N
603	Comercio al por menor de regalos	accesorios de cuero y piel, comercio al por menor especializado a través de métodos tradicionales o por internet en tiendas de regalos, artículos de uso doméstico, comercio al por menor especializado a través de métodos tradicionales o por internet en tiendas de regalos, artículos de uso personal, comercio al por menor especializado a través de métodos tradicionales o por internet en tiendas de regalos, artículos deportivos, comercio al por menor especializado a través de métodos tradicionales o	t	\N	\N
604	Comercio al por menor de artículos religiosos	accesorios y utensilios nuevos para ceremonias sacramentales, comercio al por menor especializado a través de métodos tradicionales o por internet, albas nuevas para acólitos, comercio al por menor especializado a través de métodos tradicionales o por internet, amitos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos religiosos artesanales nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos 	t	\N	\N
605	Comercio al por menor de artículos desechables	bolsas de plástico (excepto para basura), comercio al por menor especializado a través de métodos tradicionales o por internet, charolas desechables, comercio al por menor especializado a través de métodos tradicionales o por internet, conos desechables para agua, comercio al por menor especializado a través de métodos tradicionales o por internet, cubiertos desechables, comercio al por menor especializado a través de métodos tradicionales o por internet, moldes desechables, comercio al por meno	t	\N	\N
606	Comercio al por menor en tiendas de artesanías	accesorios de vestir artesanales nuevos, comercio al por menor a través de métodos tradicionales o por internet en tiendas de artesanías, adornos artesanales nuevos para casa, comercio al por menor a través de métodos tradicionales o por internet en tiendas de artesanías, alfombras artesanales nuevas, comercio al por menor a través de métodos tradicionales o por internet en tiendas de artesanías, alhajeros artesanales nuevos, comercio al por menor a través de métodos tradicionales o por internet	t	\N	\N
607	Comercio al por menor de otros artículos de uso personal	accesorios nuevos para cunas de bebés, comercio al por menor especializado a través de métodos tradicionales o por internet, amuletos, comercio al por menor especializado a través de métodos tradicionales o por internet, andaderas nuevas para bebés, comercio al por menor especializado a través de métodos tradicionales o por internet, arneses nuevos para bebés, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos nuevos para bebés, comercio al por menor 	t	\N	\N
608	Comercio al por menor de muebles para el hogar	antecomedores, comercio al por menor especializado a través de métodos tradicionales o por internet, armarios nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, bases para colchón, comercio al por menor especializado a través de métodos tradicionales o por internet, biombos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, burós nuevos, comercio al por menor especializado a través de métodos tradicionales o po	t	\N	\N
609	Comercio al por menor de electrodomésticos menores y aparatos de línea blanca	aparatos de aire acondicionado domésticos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, aparatos de calefacción domésticos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, aparatos de línea blanca nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, aparatos de ventilación domésticos nuevos, comercio al por menor especializado a través de métodos tradicionales o p	t	\N	\N
610	Comercio al por menor de muebles para jardín	bancas nuevas para jardín, comercio al por menor especializado a través de métodos tradicionales o por internet, kioscos nuevos para jardín, comercio al por menor especializado a través de métodos tradicionales o por internet, mesas nuevas para jardín, comercio al por menor especializado a través de métodos tradicionales o por internet, muebles artesanales nuevos para jardín, comercio al por menor especializado a través de métodos tradicionales o por internet, muebles de hierro nuevos para jardí	t	\N	\N
611	Comercio al por menor de cristalería, loza y utensilios de cocina	azucareras nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, baterías de cocina de aluminio nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, baterías de cocina de peltre nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, baterías de cocina nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, cacerolas nuevas, comercio al por 	t	\N	\N
612	Comercio al por menor de mobiliario, equipo y accesorios de cómputo	accesorios de cómputo nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios nuevos para computadora, comercio al por menor especializado a través de métodos tradicionales o por internet, baterías para computadoras portátiles, comercio al por menor especializado a través de métodos tradicionales o por internet, bocinas nuevas para computadora, comercio al por menor especializado a través de métodos tradicionales o por internet, cables para comput	t	\N	\N
613	Comercio al por menor de teléfonos y otros aparatos de comunicación	accesorios telefónicos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, adaptadores telefónicos nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, alarmas nuevas de uso residencial, comercio al por menor especializado a través de métodos tradicionales o por internet, antenas de radioaficionados nuevas para teléfonos, comercio al por menor especializado a través de métodos tradicionales o por internet, antenas	t	\N	\N
614	Comercio al por menor de alfombras, cortinas, tapices y similares	alfombras artesanales nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, alfombras nuevas de jardín, comercio al por menor especializado a través de métodos tradicionales o por internet, alfombras nuevas de tránsito pesado y medio, comercio al por menor especializado a través de métodos tradicionales o por internet, alfombras nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, alfombras persas y orientales nueva	t	\N	\N
615	Comercio al por menor de plantas y flores naturales	árboles naturales frutales, comercio al por menor especializado a través de métodos tradicionales o por internet, árboles naturales no frutales, comercio al por menor especializado a través de métodos tradicionales o por internet, árboles naturales, comercio al por menor especializado a través de métodos tradicionales o por internet, arreglos con naturaleza muerta, comercio al por menor especializado a través de métodos tradicionales o por internet, arreglos de frutas naturales con vinos, comerc	t	\N	\N
616	Comercio al por menor de antigüedades y obras de arte	accesorios decorativos antiguos valiosos, comercio al por menor especializado a través de métodos tradicionales o por internet, alacenas antiguas valiosas, comercio al por menor especializado a través de métodos tradicionales o por internet, álbumes de timbres postales de colección, comercio al por menor especializado a través de métodos tradicionales o por internet, antigüedades, comercio al por menor especializado a través de métodos tradicionales o por internet, billetes de colección, comerci	t	\N	\N
617	Comercio al por menor de lámparas ornamentales y candiles	arbotantes nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, candelabros ornamentales nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, candiles nuevos de cuentas de cristal cortado, comercio al por menor especializado a través de métodos tradicionales o por internet, candiles nuevos de cuentas de plástico, comercio al por menor especializado a través de métodos tradicionales o por internet, candiles nuevos d	t	\N	\N
618	Comercio al por menor de otros artículos para la decoración de interiores	árboles de navidad artificiales nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, arreglos de flores artificiales nuevas para eventos, comercio al por menor especializado a través de métodos tradicionales o por internet, arreglos de flores y plantas artificiales nuevas de migajón, comercio al por menor especializado a través de métodos tradicionales o por internet, arreglos de flores y plantas artificiales nuevas de papel recubierto, comercio al por me	t	\N	\N
619	Comercio al por menor de artículos usados	accesorios de vestir usados, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios usados de instrumentos musicales, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios usados para mascotas, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios y refacciones usadas de equipo de cómputo, comercio al por menor especializado a través de métodos tradicionales o por inter	t	\N	\N
620	Comercio al por menor en ferreterías y tlapalerías	abrasivos, comercio al por menor a través de métodos tradicionales o por internet en ferreterías y tlapalerías, accesorios de baño, comercio al por menor a través de métodos tradicionales o por internet en ferreterías y tlapalerías, accesorios para albercas, comercio al por menor a través de métodos tradicionales o por internet en ferreterías y tlapalerías, accesorios para baño, comercio al por menor a través de métodos tradicionales o por internet en ferreterías y tlapalerías, adhesivos y pegaz	t	\N	\N
621	Comercio al por menor de pisos y recubrimientos cerámicos	accesorios para baño, comercio al por menor especializado a través de métodos tradicionales o por internet, asientos para baño, comercio al por menor especializado a través de métodos tradicionales o por internet, azulejos cerámicos, comercio al por menor especializado a través de métodos tradicionales o por internet, baldosas cerámicas, comercio al por menor especializado a través de métodos tradicionales o por internet, bidés, comercio al por menor especializado a través de métodos tradicional	t	\N	\N
622	Comercio al por menor de pintura	accesorios (no artísticos) para pintar muebles e inmuebles, comercio al por menor especializado a través de métodos tradicionales o por internet, acetona, comercio al por menor especializado a través de métodos tradicionales o por internet, aguarrás, comercio al por menor especializado a través de métodos tradicionales o por internet, anilinas para pintar muebles e inmuebles, comercio al por menor especializado a través de métodos tradicionales o por internet, barnices para pintar muebles e inmu	t	\N	\N
623	Comercio al por menor de vidrios y espejos	bloques de vidrio (vidrio blocks), comercio al por menor especializado a través de métodos tradicionales o por internet, cancelería de aluminio, comercio al por menor especializado a través de métodos tradicionales o por internet, cristales (excepto para automóviles, camionetas y camiones), comercio al por menor especializado a través de métodos tradicionales o por internet, cristales antibalas, comercio al por menor especializado a través de métodos tradicionales o por internet, cristales antir	t	\N	\N
624	Comercio al por menor de artículos para la limpieza	aromatizantes, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos de jarciería, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos de limpieza artesanales, comercio al por menor especializado a través de métodos tradicionales o por internet, artículos para la limpieza, comercio al por menor especializado a través de métodos tradicionales o por internet, bandejas, comercio al por menor especializado a través	t	\N	\N
625	Comercio al por menor de materiales para la construcción en tiendas de autoservicio especializadas	accesorios para baño, comercio al por menor a través de métodos tradicionales o por internet en tiendas de autoservicio especializadas, alambres, comercio al por menor a través de métodos tradicionales o por internet en tiendas de autoservicio especializadas, alambrones, comercio al por menor a través de métodos tradicionales o por internet en tiendas de autoservicio especializadas, alfombras, comercio al por menor a través de métodos tradicionales o por internet en tiendas de autoservicio espec	t	\N	\N
626	Comercio al por menor de artículos para albercas y otros artículos	abrillantadores para albercas, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios de limpieza para albercas, comercio al por menor especializado a través de métodos tradicionales o por internet, accesorios empotrables para albercas, comercio al por menor especializado a través de métodos tradicionales o por internet, aldabas, comercio al por menor especializado a través de métodos tradicionales o por internet, alguicidas para albercas, comercio al po	t	\N	\N
627	Comercio al por menor de automóviles y camionetas nuevos	agencias de automóviles nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet en, automóviles nuevos combinado con camiones nuevos, comercio al por menor especializado a través de métodos tradicionales o por internet, automóviles nuevos compactos populares, comercio al por menor especializado a través de métodos tradicionales o por internet, automóviles nuevos de lujo, comercio al por menor especializado a través de métodos tradicionales o por internet, aut	t	\N	\N
628	Comercio al por menor de automóviles y camionetas usados	automóviles usados combinado con camiones usados, comercio al por menor especializado a través de métodos tradicionales o por internet, automóviles usados compactos populares, comercio al por menor especializado a través de métodos tradicionales o por internet, automóviles usados de lujo, comercio al por menor especializado a través de métodos tradicionales o por internet, automóviles usados de usos múltiples, comercio al por menor especializado a través de métodos tradicionales o por internet, 	t	\N	\N
629	Comercio al por menor de partes y refacciones nuevas para automóviles, camionetas y camiones	acumuladores nuevos para automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, alarmas nuevas para automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, alfombras nuevas para automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, alternadores nuevos para automóviles, camionetas y camiones, comerc	t	\N	\N
630	Comercio al por menor de partes y refacciones usadas para automóviles, camionetas y camiones	acumuladores usados o reconstruidos para automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, alarmas usadas o reconstruidas para automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, alfombras usadas o reconstruidas para automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, alternadores usados	t	\N	\N
631	Comercio al por menor de llantas y cámaras para automóviles, camionetas y camiones	cámaras nuevas para llantas de automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, corbatas nuevas para llantas de automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, llantas nuevas para automóviles, camionetas y camiones, comercio al por menor especializado a través de métodos tradicionales o por internet, plomos nuevos para llantas de automóviles, camionet	t	\N	\N
632	Comercio al por menor de motocicletas	bicimotos nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, bicimotos usadas, comercio al por menor especializado a través de métodos tradicionales o por internet, cuatrimotos nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, cuatrimotos usadas, comercio al por menor especializado a través de métodos tradicionales o por internet, llantas para motocicletas, comercio al por menor especializado a través de métod	t	\N	\N
633	Comercio al por menor de otros vehículos de motor	aeronaves nuevas para uso particular, comercio al por menor especializado a través de métodos tradicionales o por internet, aeronaves usadas para uso particular, comercio al por menor especializado a través de métodos tradicionales o por internet, avionetas nuevas, comercio al por menor especializado a través de métodos tradicionales o por internet, avionetas usadas, comercio al por menor especializado a través de métodos tradicionales o por internet, carros de carreras nuevos, comercio al por m	t	\N	\N
634	Comercio al por menor de gasolina y diésel	diésel, comercio al por menor especializado a través de métodos tradicionales o por internet, gasolina, comercio al por menor especializado a través de métodos tradicionales o por internet, gasolineras, comercio al por menor especializado a través de métodos tradicionales o por internet en	t	\N	\N
635	Comercio al por menor de gas LP en cilindros y para tanques estacionarios	gas Licuado de Petróleo (LP) en cilindros, comercio al por menor especializado a través de métodos tradicionales o por internet, gas Licuado de Petróleo (LP) para tanques estacionarios (excepto para su uso industrial), comercio al por menor especializado a través de métodos tradicionales o por internet	t	\N	\N
636	Comercio al por menor de gas LP en estaciones de carburación	estaciones de carburación, comercio al por menor especializado de gas Licuado de Petróleo (LP) a través de métodos tradicionales o por internet en, gas Licuado de Petróleo (LP) en estaciones de carburación, comercio al por menor especializado a través de métodos tradicionales o por internet	t	\N	\N
637	Comercio al por menor en estaciones de gas natural vehicular	estaciones de gas natural vehicular, comercio al por menor especializado de gas natural vehicular a través de métodos tradicionales o por internet en, gas natural vehicular en estaciones de gas natural vehicular, comercio al por menor especializado a través de métodos tradicionales o por internet	t	\N	\N
638	Comercio al por menor de otros combustibles	aserrín impregnado de combustible, comercio al por menor especializado a través de métodos tradicionales o por internet, carbón vegetal (excepto para uso industrial), comercio al por menor especializado a través de métodos tradicionales o por internet, electrolineras, comercio al por menor especializado a través de métodos tradicionales o por internet en, estaciones para recarga de vehículos eléctricos, comercio al por menor especializado a través de métodos tradicionales o por internet en, leña	t	\N	\N
639	Comercio al por menor de aceites y grasas lubricantes, aditivos y similares para vehículos de motor	aceites lubricantes de uso automotriz, comercio al por menor especializado a través de métodos tradicionales o por internet, aceites lubricantes para vehículos de motor, comercio al por menor especializado a través de métodos tradicionales o por internet, aditivos de uso automotriz, comercio al por menor especializado a través de métodos tradicionales o por internet, aditivos para vehículos de motor, comercio al por menor especializado a través de métodos tradicionales o por internet, anticongel	t	\N	\N
640	Intermediación de comercio al por menor, y comercio al por menor a través de catálogos impresos, televisión y similares	comercio de productos a través de máquinas expendedoras, comercio de productos con demostración en hogares, comercio de productos multinivel, comercio de productos por catálogo, comercio de productos puerta por puerta, intermediación de negocios a consumidores en la compra o venta de productos a través de métodos tradicionales, intermediación de negocios a consumidores en la compra o venta de productos por internet, intermediación entre consumidores en la compra o venta de productos a través de 	t	\N	\N
641	Transporte aéreo regular en líneas aéreas nacionales	automóviles y camiones ligeros, transporte aéreo regular en líneas aéreas nacionales, bienes no perecederos empacados excepto en contenedores intermodales, transporte aéreo regular en líneas aéreas nacionales, bienes perecederos empacados con clima controlado excepto en contenedores intermodales, transporte aéreo regular en líneas aéreas nacionales, carga, transporte aéreo regular en líneas aéreas nacionales, graneles secos y húmedos excepto en contenedores intermodales, transporte aéreo regular	t	\N	\N
642	Transporte aéreo regular en líneas aéreas extranjeras	automóviles y camiones ligeros, transporte aéreo regular en líneas aéreas extranjeras, bienes no perecederos empacados excepto en contenedores intermodales, transporte aéreo regular en líneas aéreas extranjeras, bienes perecederos empacados con clima controlado excepto en contenedores intermodales, transporte aéreo regular en líneas aéreas extranjeras, carga, transporte aéreo regular en líneas aéreas extranjeras, graneles secos y húmedos excepto en contenedores intermodales, transporte aéreo reg	t	\N	\N
643	Transporte aéreo no regular	aeronaves con operador para servicios de fotografía aérea, alquiler, aeronaves con operador para servicios de fumigación, alquiler, aeronaves con operador para servicios de vuelos especiales, alquiler, aerotaxis, servicios de, automóviles y camiones ligeros, transporte aéreo no regular, bienes no perecederos empacados excepto en contenedores intermodales, transporte aéreo no regular, bienes perecederos empacados con clima controlado excepto en contenedores intermodales, transporte aéreo no regul	t	\N	\N
644	Transporte por ferrocarril	animales en pie, transporte por ferrocarril, automóviles sin rodar, transporte por ferrocarril, carga, transporte por ferrocarril, carga, transporte por ferrocarril en carro consolidado, carga, transporte por ferrocarril en carro entero, contenedores de carga, transporte por ferrocarril, contenedores intermodales, transporte por ferrocarril, gases, transporte por ferrocarril, minerales, transporte por ferrocarril, pasajeros, transporte por ferrocarril, productos agrícolas, transporte por ferroca	t	\N	\N
645	Transporte marítimo de altura, excepto de petróleo y gas natural	animales en pie, transporte marítimo de altura, automóviles sin rodar, transporte marítimo de altura, carga general, excepto de petróleo y gas natural, transporte marítimo de altura, carga, excepto de petróleo y gas natural, transporte marítimo de altura, carga, excepto de petróleo y gas natural, transporte marítimo de altura en transbordadores, contenedores de carga, excepto de petróleo y gas natural, transporte marítimo de altura, embarcaciones de carga con tripulación para el transporte de al	t	\N	\N
646	Transporte marítimo de cabotaje, excepto de petróleo y gas natural	animales en pie, transporte marítimo de cabotaje, automóviles sin rodar, transporte marítimo de cabotaje, carga general, excepto de petróleo y gas natural, transporte marítimo de cabotaje, carga, excepto de petróleo y gas natural, transporte marítimo de cabotaje, carga, excepto de petróleo y gas natural, transporte marítimo de cabotaje en transbordadores, contenedores de carga, excepto de petróleo y gas natural, transporte marítimo de cabotaje, embarcaciones con tripulación para el transporte de	t	\N	\N
647	Transporte marítimo de petróleo y gas natural	combustóleo, transporte marítimo, combustóleo, transporte marítimo de altura, combustóleo, transporte marítimo de cabotaje, derivados del petróleo, transporte marítimo, diésel, transporte marítimo, diésel, transporte marítimo de altura, diésel, transporte marítimo de cabotaje, gas natural, transporte marítimo, gas natural, transporte marítimo de altura, gas natural, transporte marítimo de cabotaje, gasolina, transporte marítimo, gasolina, transporte marítimo de altura, gasolina, transporte marít	t	\N	\N
648	Transporte por aguas interiores	animales en pie, transporte por aguas interiores, automóviles sin rodar, transporte por aguas interiores, carga, transporte por aguas interiores, carga, transporte por canales, carga, transporte por lagos, carga, transporte por lagunas, carga, transporte por presas, carga, transporte por ríos, embarcaciones de pasajeros con tripulación para el transporte por aguas interiores, alquiler, pasajeros, taxi acuático por aguas interiores, pasajeros, transbordadores por aguas interiores, pasajeros, tran	t	\N	\N
649	Autotransporte local de productos agrícolas sin refrigeración	flores frescas empacadas, autotransporte local en cajas secas cerradas sin refrigeración, flores frescas empacadas, autotransporte local en camiones de redilas sin refrigeración, flores frescas empacadas, autotransporte local en contenedores sin refrigeración, flores frescas empacadas, autotransporte local en remolques sin refrigeración, flores frescas empacadas, autotransporte local en semirremolques sin refrigeración, flores frescas en cajas, autotransporte local en camiones de redilas sin ref	t	\N	\N
650	Otro autotransporte local de carga general	alimentos empacados para animales, autotransporte local, alimentos sueltos para animales, autotransporte local, carga general empacada o suelta, excepto productos agrícolas, autotransporte local en camión completo (TL) sin refrigeración, carga general empacada o suelta, excepto productos agrícolas, autotransporte local en camión consolidado (LTL) sin refrigeración, carga general empacada, excepto productos agrícolas, autotransporte local, carga general empacada, excepto productos agrícolas, auto	t	\N	\N
651	Autotransporte foráneo de productos agrícolas sin refrigeración	flores frescas empacadas, autotransporte foráneo en cajas secas cerradas sin refrigeración, flores frescas empacadas, autotransporte foráneo en camiones de redilas sin refrigeración, flores frescas empacadas, autotransporte foráneo en contenedores sin refrigeración, flores frescas empacadas, autotransporte foráneo en remolques sin refrigeración, flores frescas empacadas, autotransporte foráneo en semirremolques sin refrigeración, flores frescas en cajas, autotransporte foráneo en camiones de red	t	\N	\N
652	Otro autotransporte foráneo de carga general	alimentos empacados para animales, autotransporte foráneo, alimentos sueltos para animales, autotransporte foráneo, carga general empacada o suelta, excepto productos agrícolas, autotransporte foráneo en camión completo (TL) sin refrigeración, carga general empacada o suelta, excepto productos agrícolas, autotransporte foráneo en camión consolidado (LTL) sin refrigeración, carga general empacada, excepto productos agrícolas, autotransporte foráneo, carga general empacada, excepto productos agríc	t	\N	\N
653	Servicios de mudanzas	enseres domésticos, autotransporte foráneo, enseres domésticos, autotransporte local, equipo comercial, autotransporte foráneo en mudanzas, equipo comercial, autotransporte local en mudanzas, equipo de oficina, autotransporte foráneo en mudanzas, equipo de oficina, autotransporte local en mudanzas, equipo electrónico , autotransporte foráneo en mudanzas, equipo electrónico, autotransporte local en mudanzas, maquinaria, autotransporte foráneo en mudanzas, maquinaria, autotransporte local en mudan	t	\N	\N
654	Autotransporte local de materiales para la construcción	arena, autotransporte local, cemento en sacos, autotransporte local, concreto premezclado, autotransporte local, grava, autotransporte local, ladrillos, autotransporte local, madera para la construcción, autotransporte local, materiales metálicos para la construcción, autotransporte local, materiales no metálicos para la construcción, autotransporte local, materiales para la construcción, autotransporte local, piezas preconstruidas de materiales metálicos para la construcción, autotransporte loc	t	\N	\N
655	Autotransporte local de materiales y residuos peligrosos	explosivos, autotransporte local, gases comprimidos, autotransporte local, gases corrosivos, autotransporte local, gases disueltos a presión, autotransporte local, gases explosivos, autotransporte local, gases inflamables, autotransporte local, gases irritantes, autotransporte local, gases licuados, autotransporte local, gases refrigerados, autotransporte local, gases tóxicos, autotransporte local, gases venenosos, autotransporte local, líquidos corrosivos, autotransporte local, líquidos explosi	t	\N	\N
656	Autotransporte local con refrigeración	chapopote, autotransporte local, flores naturales frescas que requieren refrigeración, autotransporte local, materias primas comestibles que requieren refrigeración o congelación, autotransporte local, materias primas perecederas que requieren refrigeración o congelación, autotransporte local, productos agrícolas que requieren refrigeración o congelación, autotransporte local, productos agrícolas refrigerados, autotransporte local, productos cárnicos que requieren refrigeración o congelación, au	t	\N	\N
657	Autotransporte local de madera	aserrín, autotransporte local, madera aserrada, autotransporte local, madera, excepto para la construcción, autotransporte local, pulpa de madera, autotransporte local, rollos de papel laminado, autotransporte local, trocería de madera, autotransporte local, troncos, autotransporte local	t	\N	\N
658	Otro autotransporte local de carga especializado	animales en pie, autotransporte local, automóviles sin rodar, autotransporte local, basura sin recolección, autotransporte local, maquinaria pesada, autotransporte local, maquinaria sobredimensionada, autotransporte local, materiales reciclables, autotransporte local, productos sobredimensionados, autotransporte local, remolque local de casas móviles, servicios de, residuos no peligrosos de la construcción y la demolición, autotransporte local, residuos no peligrosos sin recolección, autotranspo	t	\N	\N
659	Autotransporte foráneo de materiales para la construcción	arena, autotransporte foráneo, cemento en sacos, autotransporte foráneo, concreto premezclado, autotransporte foráneo, grava, autotransporte foráneo, ladrillos, autotransporte foráneo, madera para la construcción, autotransporte foráneo, materiales metálicos para la construcción, autotransporte foráneo, materiales no metálicos para la construcción, autotransporte foráneo, materiales para la construcción, autotransporte foráneo, piezas preconstruidas de materiales metálicos para la construcción, 	t	\N	\N
660	Autotransporte foráneo de materiales y residuos peligrosos	explosivos, autotransporte foráneo, gases comprimidos, autotransporte foráneo, gases corrosivos, autotransporte foráneo, gases disueltos a presión, autotransporte foráneo, gases explosivos, autotransporte foráneo, gases inflamables, autotransporte foráneo, gases irritantes, autotransporte foráneo, gases licuados, autotransporte foráneo, gases refrigerados, autotransporte foráneo, gases tóxicos, autotransporte foráneo, gases venenosos, autotransporte foráneo, líquidos corrosivos, autotransporte f	t	\N	\N
661	Autotransporte foráneo con refrigeración	chapopote, autotransporte foráneo, flores naturales frescas que requieren refrigeración, autotransporte foráneo, materias primas comestibles que requieren refrigeración o congelación, autotransporte foráneo, materias primas perecederas que requieren refrigeración o congelación, autotransporte foráneo, productos agrícolas que requieren refrigeración o congelación, autotransporte foráneo, productos agrícolas refrigerados, autotransporte foráneo, productos cárnicos que requieren refrigeración o con	t	\N	\N
662	Autotransporte foráneo de madera	aserrín, autotransporte foráneo, madera aserrada, autotransporte foráneo, madera, excepto para la construcción, autotransporte foráneo, pulpa de madera, autotransporte foráneo, rollos de papel laminado, autotransporte foráneo, trocería de madera, autotransporte foráneo, troncos, autotransporte foráneo	t	\N	\N
663	Otro autotransporte foráneo de carga especializado	animales en pie, autotransporte foráneo, automóviles sin rodar, autotransporte foráneo, basura sin recolección, autotransporte foráneo, maquinaria pesada, autotransporte foráneo, maquinaria sobredimensionada, autotransporte foráneo, materiales reciclables, autotransporte foráneo, productos sobredimensionados, autotransporte foráneo, remolque foráneo de casas móviles, servicios de, residuos no peligrosos de la construcción y la demolición, autotransporte foráneo, residuos no peligrosos sin recole	t	\N	\N
664	Transporte colectivo urbano y suburbano de pasajeros en autobuses de ruta fija	pasajeros, transporte colectivo suburbano en autobuses, pasajeros, transporte colectivo suburbano en autobuses de ruta fija, pasajeros, transporte colectivo suburbano en autobuses de ruta metropolitana, pasajeros, transporte colectivo suburbano en autobuses de ruta metropolitana fija, pasajeros, transporte colectivo suburbano en midibuses, pasajeros, transporte colectivo suburbano en midibuses de ruta fija, pasajeros, transporte colectivo suburbano en midibuses de ruta metropolitana, pasajeros, 	t	\N	\N
665	Transporte colectivo urbano y suburbano de pasajeros en automóviles de ruta fija	pasajeros, transporte colectivo suburbano en camionetas de ruta fija, pasajeros, transporte colectivo suburbano en camionetas de ruta metropolitana fija, pasajeros, transporte colectivo suburbano en microbuses de ruta fija, pasajeros, transporte colectivo suburbano en microbuses de ruta metropolitana fija, pasajeros, transporte colectivo suburbano en minibuses de ruta metropolitana, pasajeros, transporte colectivo suburbano en minibuses de ruta metropolitana fija, pasajeros, transporte colectivo	t	\N	\N
666	Transporte colectivo urbano y suburbano de pasajeros en trolebuses y trenes ligeros	pasajeros, transporte colectivo en monorrieles, pasajeros, transporte colectivo suburbano en teleférico, pasajeros, transporte colectivo suburbano en trenes ligeros, pasajeros, transporte colectivo suburbano en trolebuses, pasajeros, transporte colectivo urbano en teleférico, pasajeros, transporte colectivo urbano en trenes ligeros, pasajeros, transporte colectivo urbano en trolebuses	t	\N	\N
669	Transporte colectivo foráneo de pasajeros de ruta fija	pasajeros, transporte colectivo foráneo de ruta fija, pasajeros, transporte colectivo foráneo en autobuses categoría económica, pasajeros, transporte colectivo foráneo en autobuses de categoría ejecutiva, pasajeros, transporte colectivo foráneo en autobuses de lujo, pasajeros, transporte colectivo foráneo en autobuses de primera clase, pasajeros, transporte colectivo foráneo en autobuses de ruta fija, pasajeros, transporte colectivo foráneo en autobuses de segunda clase, pasajeros, transporte co	t	\N	\N
670	Transporte de pasajeros en taxis de sitio	apoyo a taxis, servicios de, operadores de flotas de taxis de sitio, servicios, operadores por cuenta propia de taxis de sitio, servicios, operadores propietarios de taxis de sitio, servicios, radiotaxis, transporte de pasajeros en, servicios de transporte en vehículos solicitados por medio de una página de internet o una aplicación móvil, taxis con base fija, transporte en, taxis de aeropuerto y otras terminales de transporte foráneo, transporte, taxis de sitio, transporte de pasajeros en, taxi	t	\N	\N
671	Transporte de pasajeros en taxis de ruleteo	operadores propietarios de taxis de ruleteo, servicios, taxis de ruleteo, transporte de pasajeros en, taxis de ruleteo, transporte urbano y suburbano, taxis sin base fija, transporte	t	\N	\N
672	Alquiler de automóviles con chofer	automóviles con chofer, alquiler, automóviles de lujo con chofer, alquiler, camionetas con operador, alquiler, carroza fúnebre con operador, alquiler, limusinas con chofer, alquiler	t	\N	\N
673	Transporte escolar y de personal	operación de autobuses escolares y de personal, transporte de empleados, transporte de obreros, transporte de personal, transporte escolar	t	\N	\N
674	Alquiler de autobuses con chofer	autobuses con chofer, alquiler, autobuses y vehículos con chofer para el transporte foráneo de pasajeros sin ruta fija, alquiler	t	\N	\N
675	Otro transporte terrestre de pasajeros	pasajeros en bicitaxis, transporte de, pasajeros en mototaxis, transporte de, pasajeros en vehículos de tracción animal, transporte de, pasajeros en vehículos de tracción humana, transporte de, pasajeros minusválidos, transporte especial para, pasajeros, transporte en camiones de redilas, transporte especial sin servicio médico para ancianos, transporte especial sin servicio médico para personas con discapacidad, transporte especial sin servicio médico para personas débiles, transporte especial 	t	\N	\N
676	Transporte de petróleo crudo por ductos	petróleo crudo, transporte a través de estaciones de bombeo a presión, petróleo crudo, transporte por ductos, petróleo crudo, transporte por oleoductos	t	\N	\N
677	Transporte de gas natural por ductos	gas natural, operación de ductos para transporte, gas natural, transporte a través de estaciones de bombeo a presión, gas natural, transporte por ductos, gas natural, transporte por gasoductos	t	\N	\N
678	Transporte por ductos de productos refinados del petróleo	combustóleo, transporte por ductos, diésel, transporte por ductos, gas licuado, transporte por poliductos, gasolina, transporte por poliductos, líquidos de gas natural, transporte por ductos, petróleo refinado, transporte por ductos, productos refinados del petróleo, transporte a través de estaciones de bombeo a presión, productos refinados del petróleo, transporte por ductos	t	\N	\N
679	Transporte por ductos de otros productos, excepto de productos refinados del petróleo	carbón, transporte por ductos, estación de bombeo a presión para oleoductos, servicios de	t	\N	\N
680	Transporte turístico por tierra	autobuses panorámicos de dos pisos, transporte turístico en, autobuses, transporte turístico en, cabriolés, transporte turístico en, calandrias, transporte turístico en, calesas de tracción humana, transporte turístico en, calesas, transporte turístico en, camionetas panorámicas, transporte turístico en, carruajes, transporte turístico en, coches de tracción humana, transporte turístico en, coches tirados por caballos, transporte turístico en, excursiones panorámicas y escénicas por tierra, mono	t	\N	\N
681	Transporte turístico por agua	barcazas, transporte turístico en, botes panorámicos con operador, alquiler, botes para excursiones con operador, alquiler, botes para pesca deportiva con operador, alquiler, cruceros discoteca, transporte turístico en, cruceros restaurante, transporte turístico en, excursiones panorámicas y escénicas por agua, excursiones para observar ballenas, lanchas, transporte turístico en, operación de hidroaviones con fines turísticos, paseos panorámicos y escénicos en cruceros con servicios de alojamien	t	\N	\N
682	Otro transporte turístico	aviones, transporte turístico en, avionetas, transporte turístico en, dirigibles, transporte turístico en, excursiones panorámicas y escénicas por aire, funiculares, transporte turístico en, globos aerostáticos, transporte turístico en, helicópteros, transporte turístico en, paseos panorámicos y escénicos aéreos con servicios integrados de alimentos y entretenimiento, excepto hospedaje, paseos panorámicos y escénicos aéreos sin servicios integrados, teleféricos, transporte turístico en, tranvía 	t	\N	\N
683	Servicios a la navegación aérea	centros de control para la navegación aérea, servicios de, control de tránsito aéreo, servicios de, control de tránsito y servicios a la navegación aérea, servicios de, despacho e información de vuelos, servicios de, indicadores de rumbo y posición para aeronaves, servicios de, meteorología aeronáutica, servicios de, meteorología para la navegación aérea, servicios de, navegación aérea, servicios de, provisión de información aeronáutica, servicios de, provisión de información sobre tránsito aére	t	\N	\N
684	Administración de aeropuertos y helipuertos	administración de aeropuertos y helipuertos, administración de edificios del aeropuerto, administración de edificios del helipuerto, administración de pistas de aterrizaje, administración de plataformas aéreas, administración y operación de aeropuertos, aterrizaje de aeronaves, servicios de, carga y descarga de equipaje en los aviones, servicios de, carga y descarga de mercancías en los aviones, servicios de, conservación de aeropuertos y helipuertos, servicios de, conservación de edificios del 	t	\N	\N
685	Otros servicios relacionados con el transporte aéreo	aeronaves privadas, administración de, aeronaves privadas, administración y operación de, aeronaves y helicópteros, reparación y mantenimiento, aeronaves, inspección, aeronaves, lavado, aeronaves, limpieza exterior, aeronaves, reparación y mantenimiento, aerotaxis, reparación y mantenimiento, alfombras de aeronaves, inspección y cambio, asientos de aeronaves, inspección y reparación, componentes de aeronaves, mantenimiento, comprobación y reparación de la iluminación de la cabina de pasajeros de	t	\N	\N
686	Servicios relacionados con el transporte por ferrocarril	administración de estaciones y terminales de ferrocarril, birlos del motor de máquina de ferrocarril, mantenimiento, carga y descarga de equipaje en ferrocarriles, servicios de, carga y descarga de mercancías en ferrocarriles, servicios de, carretones para ferrocarriles, limpieza y mantenimiento, carros de carga de ferrocarril, limpieza exterior, carros de ferrocarril, limpieza exterior, carros de ferrocarril, reparación, cojinetes de ferrocarriles, limpieza y mantenimiento, derecho de paso en v	t	\N	\N
687	Administración de puertos y muelles	administración de puertos y muelles, escolleras, mantenimiento, espigones, mantenimiento, instalaciones portuarias, servicios de, muelles, mantenimiento, operación de atracaderos, operación de canales, operación de embarcaderos, operación de faros, operación de muelles, operación de puertos, operación de terminales portuarias de pasajeros, operación de varaderos, operación de vías marítimas, patios en muelles para contenedores, mantenimiento, patios en muelles para vehículos, mantenimiento, puer	t	\N	\N
688	Servicios de carga y descarga para el transporte por agua	alijadores en puerto, servicios de, carga dentro del puerto, servicios de, carga general en puerto, servicios de, carga y descarga de equipaje en las embarcaciones, servicios de, carga y descarga de fluidos en puerto, servicios de, carga y descarga de minerales en puerto, servicios de, carga y descarga de petróleo y sus derivados en puerto, servicios de, carga y descarga de productos agrícolas en puerto, servicios, carga y descarga para el transporte por agua, servicios de, descarga dentro del p	t	\N	\N
689	Servicios para la navegación por agua	amarre de cabos, servicios de, atraque de embarcaciones, servicios de, control de tránsito de embarcaciones en puertos, servicios de, desamarre de cabos, servicios de, desatraque de embarcaciones, servicios de, meteorología para la navegación por agua, servicios de, navegación por agua, servicios de, operación de boyas, pilotaje de buques, servicios de, plataformas, remolque marítimo de cabotaje, radiocomunicación a las embarcaciones, servicios de, reflotación de embarcaciones, servicios de, rem	t	\N	\N
690	Otros servicios relacionados con el transporte por agua	alfombras de embarcaciones, mantenimiento, asientos de embarcaciones, tapicería, avituallamiento de embarcaciones, servicios de, barcos y yates que requieren tripulación, reparación, mantenimiento y conversión, checador de carga marítima, servicios de, descamación de embarcaciones fuera de astilleros, servicios de, desmantelamiento de embarcaciones en diques secos flotantes, servicios de, embarcaciones, inspección, equipo de transporte por agua, reparación y mantenimiento de, extracción de aguas	t	\N	\N
691	Servicios de grúa	arrastre de vehículos automotores, servicios de, grúas para automotores, servicios de, remolque de automóviles averiados, servicios de, remolque de camiones averiados, servicios de	t	\N	\N
692	Servicios de administración de centrales camioneras	administración de centrales camioneras, administración de terminales para el autotransporte de carga, carga y descarga de autobuses, servicios de, centrales camioneras, mantenimiento, centrales camioneras, servicios de, control de tránsito dentro de la terminal de camiones, servicios de, inspección y verificación para el comercio exterior de carga, servicios de, manejo de equipaje dentro de la central camionera, servicios de, operación de centrales camioneras, operación de terminales para el aut	t	\N	\N
693	Servicios de administración de carreteras, puentes y servicios auxiliares	administración de autopistas de cobro, administración de carreteras y puentes, auxilio vial en carreteras, servicios de, carreteras, limpieza de, cobro de la tarifa por uso de carreteras y puentes, operación de autopistas de casetas de cobro, operación de paradores, operación de puentes de casetas de cobro, operación de túneles de casetas de cobro, señalamientos de carreteras, mantenimiento	t	\N	\N
694	Servicios de báscula para el transporte y otros servicios relacionados con el transporte por carretera	arrastre de contenedores, servicios de, auxilio carretero para vehículos automotores, básculas eléctricas para el autotransporte, servicios de, básculas electrónicas para el autotransporte, servicios de, básculas mecánicas de usos especiales para el autotransporte, servicios de, básculas mecánicas para el autotransporte, servicios de, básculas para el autotransporte, servicios de, calles y caminos, limpieza de, conducción de vehículos automotores para su entrega, servicios de, inspección de carg	t	\N	\N
695	Servicios de agencias aduanales	agencias aduanales, servicios aduanales, tramitación para la exportación de mercancías, tramitación para la importación de mercancías	t	\N	\N
696	Otros servicios de intermediación para el transporte de carga	agencias consignatarias, agencias consolidadoras de carga, agencias de carga, agencias de embarque y desembarque de carga, agencias navieras, agencias reexpedidoras de carga, consolidación de carga, coordinación para el autotransporte de carga, servicios de, coordinación para el transporte aéreo de carga, servicios de, coordinación para el transporte ferroviario de carga, servicios de, coordinación para el transporte por agua de carga, servicios de, corretaje de carga, servicios de, intermediaci	t	\N	\N
697	Otros servicios relacionados con el transporte	administración integral de sistemas de tarjetas para uso en el transporte público de pasajeros, embalaje y desembalaje de carga para su transportación, servicios de, empaque de carga para su transporte, servicios de, envasado y desenvasado de productos para su transporte, servicios de, flejado de productos para su transporte, licuefacción de gas con fines de transporte, verificación de rutas y horarios para transporte de pasajeros, servicios de	t	\N	\N
698	Servicios postales	apartados postales del sector público, servicios de, buzones express, servicio de, certificación de correspondencia, servicios de, correo de porte pagado, servicios de, correo de publicaciones periódicas, servicios de, correo despacho inmediato, servicios de, correo reembolso, servicios de, correo tradicional, servicios de, envío de correspondencia con acuse de recibo, servicios de, envío de correspondencia con derechos por cobrar, servicios de, envío de correspondencia internacional, servicios 	t	\N	\N
699	Servicios de mensajería y paquetería foránea	mensajería foránea, mensajería foránea con recolección y entrega a domicilio, mensajería foránea en servicio ocurre, mensajería internacional, mensajería nacional, mensajería y paquetería foránea, paquetería foránea, servicio de, paquetería internacional, servicio de, paquetería nacional, servicio de	t	\N	\N
700	Servicios de mensajería y paquetería local	entrega local de alimentos solicitados por medio de métodos tradicionales o de una página de internet o una aplicación, servicios de, entrega local de medicinas solicitadas por medio de métodos tradicionales o de una página de internet o una aplicación, servicios de, entrega local de pedidos solicitados por medio de métodos tradicionales o de una página de internet o una aplicación, servicios de, entrega local de pizzas solicitadas por medio de métodos tradicionales o de una página de internet o	t	\N	\N
701	Almacenes generales de depósito	almacenamiento en recintos fiscales, almacenamiento general con bono en prenda, almacenamiento general con expedición de certificados de depósito, almacenes generales de depósito, servicios de	t	\N	\N
702	Otros servicios de almacenamiento general sin instalaciones especializadas	almacenamiento general sin instalaciones especializadas, carga empacada, almacenamiento que no requiere instalaciones especiales, carga suelta, almacenamiento que no requiere instalaciones especiales, pallets de refrescos, almacenamiento que no requiere instalaciones especiales, productos de papel, almacenamiento que no requiere instalaciones especiales, tubos y rollos de acero, almacenamiento que no requiere instalaciones especiales	t	\N	\N
706	Producción de películas	estudios cinematográficos, servicios de, estudios de filmación, servicios de, películas cinematográficas educativas, producción, películas cinematográficas, producción, películas cinematográficas, producción integrada con la distribución, películas de cortometraje, producción, películas de largometraje, producción, películas en formato de video, producción, películas en formato de video, producción integrada con la distribución	t	\N	\N
707	Producción de programas para la televisión	dibujos animados para la televisión, producción, noticieros para la televisión, producción, películas educativas para la televisión, producción, programas de concurso para la televisión, producción, programas documentales para la televisión, producción, programas infantiles para la televisión, producción, programas para la televisión, producción, series para la televisión, producción, telenovelas para la televisión, producción	t	\N	\N
708	Producción de videoclips, comerciales y otros materiales audiovisuales	comerciales para la televisión, producción, material audiovisual educativo, producción, material audiovisual, producción, spots promocionales, producción, videoclips, producción, videoclips, producción integrada con la distribución, videos de capacitación, producción, videos de tipo empresarial, producción, videos musicales, producción integrada con la distribución	t	\N	\N
709	Distribución de películas y de otros materiales audiovisuales	agencias de distribución de películas con licenciamiento, distribución con licenciamiento de películas, distribución de obras audiovisuales incluyendo su reproducción, distribución de obras audiovisuales sin reproducción, material audiovisual, distribución con licenciamiento, películas cinematográficas extranjeras, distribución con licenciamiento, películas cinematográficas nacionales, distribución con licenciamiento, películas cinematográficas, distribución con licenciamiento, películas en form	t	\N	\N
710	Exhibición de películas y otros materiales audiovisuales	admisión a salas de exhibición cinematográfica, autocinemas, servicios de, cines, servicios de, exhibición de películas que en la misma ubicación física venden dulces y otros alimentos bajo la misma razón social, material audiovisual, exhibición, organización de festivales cinematográficos, películas cinematográficas nacionales y extranjeras, exhibición, películas de video, exhibición, películas en aerolíneas, exhibición, películas en formato de cine, exhibición, películas en formato de video, e	t	\N	\N
711	Servicios de postproducción y otros servicios para la industria fílmica y del video	agencias de reservación de películas cinematográficas, servicios de, animación cinematográfica, animación para programas de televisión, servicios de, autoría en DVD, closed captioning para películas, closed captioning para programas de televisión, closed captioning para videoclips, conversión de formato fílmico, crestomatía, servicios de, efectos especiales para comerciales, efectos especiales para películas, efectos especiales para producciones cinematográficas, efectos especiales para programa	t	\N	\N
712	Editoras de música	administración de derechos de autor de obras musicales, administración, promoción y autorización del uso de composiciones musicales, canciones, edición, canciones, edición integrada con la impresión, editoras de música, servicios de, libros musicales, edición integrada con la impresión, licenciamiento de música protegida por derechos de autor, partituras, edición, partituras, edición integrada con la impresión	t	\N	\N
713	Grabación de discos compactos (CD) y de video digital (DVD) o casetes musicales	casetes, grabación de material sonoro, cintas magnetofónicas, grabación de material sonoro, discos de video digital (DVD) musicales, grabación, discos, grabación de material sonoro, diseño de efectos sonoros para obras audiovisuales, estudios de grabación con operador, alquiler, estudios de grabación, servicios de, grabación de material musical en estudio excluyendo la mezcla de efectos sonoros, grabación de material musical en estudio incluyendo la mezcla de efectos sonoros, masterización de gr	t	\N	\N
714	Productoras y distribuidoras discográficas	casetes musicales, producción de material discográfico en, casetes musicales, producción de material discográfico integrada con su distribución, casetes musicales, producción de material discográfico integrada con su reproducción, casetes musicales, producción de material discográfico integrada con su reproducción y distribución, compañías discográficas integradas, discos compactos (CD) y cintas de audio pregrabadas, reproducción integrada con su lanzamiento, y su distribución, discos compactos 	t	\N	\N
715	Otros servicios de grabación del sonido	audiograbación en estudio de programas radiofónicos, audiograbación en vivo de conferencias y seminarios, audiolibros, grabación, comerciales radiofónicos, grabación no realizada por las estaciones radiofónicas, conferencias, audiograbación, material autodidáctico, audiograbación, material educativo, audiograbación, música de archivo, audiograbación, programas radiofónicos, grabación no realizada por las estaciones radiofónicas, reuniones, audiograbación	t	\N	\N
716	Edición de periódicos en formato electrónico	periódicos de información especializada, edición en formato electrónico, periódicos de información especializada, edición y difusión exclusivamente a través de internet, periódicos de información general, edición en formato electrónico, periódicos de información general, edición y difusión exclusivamente a través de internet, periódicos, edición en formato electrónico, periódicos, edición y difusión exclusivamente a través de internet	t	\N	\N
717	Edición de periódicos integrada con la impresión	periódicos de información especializada, edición integrada con la impresión en papel, periódicos de información especializada, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, periódicos de información general, edición integrada con la impresión en papel, periódicos de información general, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, periódicos, edición integrada con la impresión en papel, periódicos, e	t	\N	\N
718	Edición de revistas y otras publicaciones periódicas en formato electrónico	boletines informativos, edición en formato electrónico, boletines informativos, edición y difusión exclusivamente a través de internet, boletines que únicamente anuncian bienes o servicios, edición en formato electrónico, comics, edición en formato electrónico, diarios escolares, edición en formato electrónico, diarios escolares, edición y difusión exclusivamente a través de internet, guías de radio, edición en formato electrónico, guías de radio, edición y difusión exclusivamente a través de in	t	\N	\N
733	Otros servicios de telecomunicaciones	acceso a internet a través de conexiones de telecomunicaciones proporcionadas por el cliente, operación de estaciones de radar, rastreo de satélites, recarga electrónica de tiempo aire (tiempo aire electrónico), redes privadas sobre infraestructura del cliente, servicios de, redes virtuales móviles (MVNO), reventa (distribución) de tarjetas telefónicas prepagadas, reventa de servicios de telecomunicaciones alámbricas, reventa de servicios de telecomunicaciones excepto satelitales, reventa de ser	t	\N	\N
719	Edición de revistas y otras publicaciones periódicas integrada con la impresión	boletines informativos, edición integrada con la impresión en papel, boletines informativos, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, boletines que únicamente anuncian bienes o servicios, edición integrada con la impresión en papel, boletines que únicamente anuncian bienes o servicios, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, comics, edición integrada con la impresión en papel, comics, edici	t	\N	\N
720	Edición de libros en formato electrónico	almanaques, edición en formato electrónico, almanaques, edición y difusión exclusivamente a través de internet, atlas, edición en formato electrónico, atlas, edición y difusión exclusivamente a través de internet, audio libros, edición en formato electrónico, diccionarios, edición en formato electrónico, diccionarios, edición y difusión exclusivamente a través de internet, enciclopedias, edición en formato electrónico, enciclopedias, edición y difusión exclusivamente a través de internet, guías 	t	\N	\N
721	Edición de libros integrada con la impresión	almanaques, edición integrada con la impresión en papel, almanaques, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, atlas, edición integrada con la impresión en papel, atlas, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, diccionarios, edición integrada con la impresión en papel, diccionarios, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, enciclopedias, ed	t	\N	\N
722	Edición de directorios y listas de correo en formato electrónico	bases de datos de propietarios de medicamentos, edición en formato electrónico, bases de datos de registros públicos, edición en formato electrónico, bases de datos de resultados de casos legales, edición en formato electrónico, bases de datos sobre registro de patentes, edición en formato electrónico, bases de datos, edición en formato electrónico, bases de datos, edición y difusión exclusivamente a través de internet, colecciones de información de registros públicos, edición en formato electró	t	\N	\N
723	Edición de directorios y listas de correo integrada con la impresión	bases de datos de propietarios de medicamentos, edición integrada con la impresión en papel, bases de datos de propietarios de medicamentos, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, bases de datos de registros públicos, edición integrada con la impresión en papel, bases de datos de registros públicos, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, bases de datos de resultados de casos legales, edi	t	\N	\N
724	Edición de otros materiales en formato electrónico	agendas, edición en formato electrónico, anuarios, edición en formato electrónico, calendarios, edición en formato electrónico, calendarios, edición y difusión exclusivamente a través de internet, carteles, edición en formato electrónico, catálogos, edición en formato electrónico, folletos, edición en formato electrónico, formatos para apuestas o sorteos, edición en formato electrónico, libros para iluminar, edición en formato electrónico, libros para iluminar, edición y difusión exclusivamente 	t	\N	\N
725	Edición de otros materiales integrada con la impresión	agendas, edición integrada con la impresión en papel, agendas, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, anuarios, edición integrada con la impresión en papel, anuarios, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, calendarios, edición integrada con la impresión en papel, calendarios, edición integrada con la impresión en papel combinada con su difusión en formato electrónico, carteles, edición i	t	\N	\N
726	Edición de software	software de aplicación masivo o empacado, desarrollo y edición, software de aplicación masivo o empacado, desarrollo y edición integrados con su difusión en formato electrónico, software de contabilidad masivo o empacado, desarrollo y edición, software de contabilidad masivo o empacado, desarrollo y edición integrados con su difusión en formato electrónico, software de entretenimiento masivo o empacado, desarrollo y edición, software de entretenimiento masivo o empacado, desarrollo y edición int	t	\N	\N
727	Estaciones de transmisión de programas de radio	comerciales de radio mediante señal abierta, producción, transmisión y repetición, crónicas de radio mediante señal abierta, producción y transmisión, crónicas de radio mediante señal abierta, repetición, crónicas de radio mediante señal abierta, transmisión, estaciones de radio de amplitud modulada (AM), servicios de, estaciones de radio de frecuencia modulada (FM), servicios de, estaciones de radio, servicios de, estaciones radiofónicas, servicios de, estaciones retransmisoras de radio, servic	t	\N	\N
728	Estaciones de transmisión de programas de televisión	caricaturas mediante televisión de señal abierta, transmisión, estaciones de televisión mediante señal abierta, servicios de, noticieros mediante televisión de señal abierta, transmisión, películas mediante televisión de señal abierta, transmisión, programación pública y no comercial para televisión, servicios de, programas de concurso mediante televisión de señal abierta, transmisión, programas de televisión mediante señal abierta, producción y transmisión, programas de televisión mediante seña	t	\N	\N
729	Servicios de distribución de audio y video en tiempo real (streaming), redes sociales, cadenas de radio y televisión y otros proveedores de contenido	agencias noticiosas, servicios de, artículos noticiosos para medios de comunicación, recopilación, artículos noticiosos para medios de comunicación, suministro, cadenas de radio, operación de, cadenas de televisión por cable, cadenas de televisión por satélite, cadenas de televisión, operación de, contenido para adultos, edición y difusión exclusivamente a través de internet, distribución de audio en tiempo real (streaming), distribución de video en tiempo real (streaming), fotografías para medi	t	\N	\N
730	Operadores de servicios de telecomunicaciones alámbricas	acceso alámbrico a servicios de voz sobre protocolo de internet (VOIP), acceso mediante cable a internet alámbrico, antena master para televisión satelital (SMATV), servicios de, distribución de multicanales a puntos múltiples (MMDS), distribución de programas de música vía satelital, distribución por cable de programas de música, operadores de redes alámbricas, operadores de servicios de telecomunicaciones alámbricas, operadores de telecomunicaciones alámbricas por suscripción, operadores de te	t	\N	\N
731	Operadores de servicios de telecomunicaciones inalámbricas	acceso a internet inalámbrico, acceso inalámbrico a servicios de voz sobre protocolo de internet (VOIP), operadores de radiolocalizadores de personas, operadores de redes telefónicas inalámbricas, operadores de servicios de telecomunicaciones inalámbricas, operadores de telefonía celular móvil, proveedores de acceso a internet inalámbrico, provisión de sistemas de localización de personas, radiolocalización móvil de personas, servicio de, redes de telefonía celular móvil, servicios de, servicio 	t	\N	\N
734	Provisión de infraestructura de servicios de cómputo, procesamiento de datos, hospedaje de páginas de internet y otros servicios relacionados	acceso a software de aplicación que se ofrece en servidores compartidos, acceso a software de aplicación que se ofrece en servidores dedicados, administración de datos, administración de redes, administración de sistemas de computación, administración de tiendas virtuales, almacenamiento de información en computadoras, auditoría y evaluación de operaciones computacionales, bases de datos de reservaciones de boletos de avión, procesamiento, bases de datos de reservaciones de hospedaje, procesamie	t	\N	\N
735	Bibliotecas y archivos del sector privado	archivos de información de interés nacional del sector privado, servicios de, bibliotecas del sector privado, servicios de, centros de información y de documentación del sector privado, servicios de, clasificación de material de consulta en bibliotecas del sector privado, colección de material de consulta en bibliotecas del sector privado, conservación de material de consulta en bibliotecas del sector privado, consulta de archivos musicales, servicios prestados por el sector privado, filmotecas 	t	\N	\N
736	Bibliotecas y archivos del sector público	archivos de información de interés nacional del sector público, servicios de, bibliotecas del sector público, servicios de, centros de información y de documentación del sector público, servicios de, clasificación de material de consulta en bibliotecas del sector público, colección de material de consulta en bibliotecas del sector público, conservación de material de consulta en bibliotecas del sector público, consulta de archivos musicales, servicios prestados por el sector público, filmotecas 	t	\N	\N
737	Portales de búsqueda en la red y otros servicios de suministro de información	agencias de fotos de archivo, búsqueda de información a petición del cliente, búsqueda en la red, servicios de, inventarios de fotografías (stock photos), servicios de, portales de búsqueda en la red, provisión de información por teléfono mediante mensajes pregrabados, provisión de mensajes pregrabados de noticias, provisión de mensajes pregrabados sobre el estado del tiempo, provisión de mensajes pregrabados sobre horóscopos, provisión de mensajes pregrabados sobre resultados de competencias de	t	\N	\N
738	Banca central	banca central	t	\N	\N
739	Banca múltiple	administración de efectivo y cuenta de empresas o negocios, banca comercial, banca de primer piso, banca múltiple, captación de cuentas de ahorro por la banca múltiple, captación de depósitos a plazos por la banca múltiple, cartas de crédito por la banca múltiple, emisión, certificados negociables de depósito por la banca múltiple, emisión, cheques de caja por la banca múltiple, emisión, cheques de viajero por la banca múltiple, emisión, cheques por la banca múltiple, certificación de, correspon	t	\N	\N
740	Banca de desarrollo	banca de desarrollo, banca de segundo piso, cartas de crédito por la banca de desarrollo, emisión de, certificados negociables de depósito por la banca de desarrollo, emisión de, cheques de caja por la banca de desarrollo, emisión de, cheques por la banca de desarrollo, certificación de, corresponsalía bancaria por la banca de desarrollo, otorgamiento de préstamos a empresas financieras por la banca de desarrollo, otorgamiento de préstamos a gobiernos por la banca de desarrollo, otorgamiento de 	t	\N	\N
741	Fondos y fideicomisos financieros	fideicomisos financieros, fondos financieros	t	\N	\N
742	Uniones de crédito	uniones de crédito	t	\N	\N
743	Cajas, cooperativas y sociedades financieras de ahorro y préstamo popular	cajas de ahorro y préstamo popular, cooperativas de ahorro y préstamo popular, sociedades financieras de ahorro y préstamo popular	t	\N	\N
744	Otras instituciones de ahorro y préstamo	otorgamiento de créditos por otras instituciones de ahorro y préstamo	t	\N	\N
745	Compañías de autofinanciamiento	compañías de autofinanciamiento	t	\N	\N
746	Montepíos	montepíos (constituidos como instituciones de asistencia privada), servicios de	t	\N	\N
747	Casas de empeño	casas de empeño (constituidas como personas físicas o sociedades anónimas), servicios de	t	\N	\N
748	Sociedades financieras de objeto múltiple	arrendamiento financiero por sociedades financieras de objeto múltiple, factoraje con riesgo de cobro (sin recurso) por sociedades financieras de objeto múltiple, factoraje financiero por sociedades financieras de objeto múltiple, factoraje sin riesgo de cobro (con recurso) por sociedades financieras de objeto múltiple, otorgamiento de créditos garantizados a consumidores por sociedades financieras de objeto múltiple, otorgamiento de créditos hipotecarios residenciales por sociedades financieras	t	\N	\N
749	Otras instituciones de intermediación crediticia y financiera no bursátil	financiadoras, financiamiento de bienes duraderos, tarjetas de crédito no bancarias, operación y promoción	t	\N	\N
750	Servicios relacionados con la intermediación crediticia no bursátil	consultoría financiera, emisión de tarjetas de regalos, para despensas, puntos, restaurantes y gasolina, emisión de tarjetas electrónicas tipo vales de despensa como beneficio para empleados, procesamiento de transacciones vinculadas con tarjetas de crédito bancarias, promoción y negociación de operaciones en el mercado nacional, representación de instituciones financieras extranjeras, validación de cheques, servicios de\n	t	\N	\N
751	Casas de bolsa	casas de bolsa, servicios de, colocación, compra y venta de acciones, colocación, compra y venta de instrumentos de deuda, colocación, compra y venta de valores, comercialización de valores corporativos, compra y venta de certificados de aportación (CAPS), compra y venta de futuros negociados dentro de la bolsa, compra y venta de opciones negociadas dentro de la bolsa, compra y venta de recibos de aceptaciones de depósitos (ADR´S), intermediación bursátil de Aceptaciones bancarias por casas de b	t	\N	\N
752	Casas de cambio	casas de cambio, servicios de, operaciones cambiarias orientadas a los mercados interbancario y corporativo	t	\N	\N
753	Centros cambiarios	centros cambiarios, servicios de, comercialización y corretaje de monedas digitales o virtuales, compraventa de monedas digitales o virtuales por internet, operaciones cambiarias orientadas al público en general (operaciones de ventanilla)	t	\N	\N
754	Bolsa de valores	acceso a sistemas de comercialización de valores, bolsa de valores, servicios de, listado en el mercado de valores, mercado de valores, administración, regulación de operaciones bursátiles	t	\N	\N
755	Asesoría en inversiones	agentes independientes en consultoría en inversiones para el mercado de valores, servicios de, asesoría en inversiones, asesoría en inversiones en el mercado de valores	t	\N	\N
756	Otros servicios relacionados con la intermediación bursátil	cámaras de compensación de monedas digitales o virtuales, ejecución, liquidación y compensación de valores, instituciones para el depósito de valores, sociedades operadoras de sociedades de inversión	t	\N	\N
757	Compañías de seguros	aseguradoras, servicios financieros de, compañías de seguros contra accidentes, compañías de seguros contra daños, compañías de seguros contra robos, compañías de seguros de vida, compañías de seguros, servicios de, pólizas de reaseguro de daños, emisión, pólizas de reaseguro de vida, accidentes, enfermedades y renta vitalicia, emisión, pólizas de seguros a comercios y riesgos múltiples, emisión, pólizas de seguros a propietarios de casas y riesgos múltiples, emisión, pólizas de seguros contra a	t	\N	\N
758	Fondos de aseguramiento campesino	compañías de seguros agrícolas, fondos de aseguramiento campesino, pólizas de seguros de agricultura y riesgos múltiples, emisión	t	\N	\N
759	Compañías afianzadoras	afianzadoras, servicios financieros de, fianzas administrativas, emisión, fianzas de fidelidad, emisión, fianzas de protección crediticia, emisión, reafianzamiento	t	\N	\N
760	Agentes, ajustadores y gestores de seguros y fianzas	agentes de fianzas, servicios de, agentes de seguros, servicios de, ajustadores de seguros, servicios de, gestores de seguros, servicios de	t	\N	\N
761	Administración de fondos para el retiro	consultoría en planes de pensión, fondos para el retiro, administración	t	\N	\N
762	Sociedades de inversión especializadas en fondos para el retiro	sociedades de inversión especializadas en fondos para el retiro	t	\N	\N
763	Fondos de inversión	fondos de inversión, fondos de inversión de capitales, fondos de inversión de objeto limitado, fondos de inversión de renta variable, fondos de inversión en instrumentos de deuda	t	\N	\N
764	Alquiler sin intermediación de viviendas amuebladas	casas amuebladas, alquiler sin intermediación, casas dúplex amuebladas, alquiler sin intermediación, casas rodantes establecidas en un sitio para ser ocupadas como vivienda, alquiler sin intermediación, condominios horizontales amueblados, alquiler sin intermediación, departamentos amueblados, alquiler sin intermediación, habitaciones amuebladas, alquiler sin intermediación, viviendas amuebladas, alquiler sin intermediación	t	\N	\N
765	Alquiler sin intermediación de viviendas no amuebladas	casas dúplex no amuebladas, alquiler sin intermediación, casas no amuebladas, alquiler sin intermediación, condominios horizontales no amueblados, alquiler sin intermediación, departamentos no amueblados, alquiler sin intermediación, habitaciones no amuebladas, alquiler sin intermediación, viviendas no amuebladas, alquiler sin intermediación	t	\N	\N
766	Alquiler sin intermediación de salones para fiestas y convenciones	centros de convenciones, alquiler sin intermediación, fincas para eventos sociales, alquiler sin intermediación, jardines para eventos sociales, alquiler sin intermediación, salones para baile, alquiler sin intermediación, salones para banquetes, alquiler sin intermediación, salones para conferencias, alquiler sin intermediación, salones para eventos sociales, alquiler sin intermediación, salones para exposiciones, alquiler sin intermediación, salones para fiestas infantiles, alquiler sin interm	t	\N	\N
767	Alquiler sin intermediación de oficinas y locales comerciales	edificios de oficinas, alquiler sin intermediación, espacios en clínicas, alquiler sin intermediación de, locales comerciales, alquiler sin intermediación, oficinas amuebladas, alquiler sin intermediación, oficinas no amuebladas, alquiler sin intermediación, oficinas virtuales, alquiler sin intermediación de	t	\N	\N
768	Alquiler sin intermediación de teatros, estadios, auditorios y similares	arenas de espectáculos, alquiler sin intermediación, auditorios, alquiler sin intermediación de, canchas al aire libre, alquiler sin intermediación, canchas techadas, alquiler sin intermediación, cines, alquiler sin intermediación, estadios, alquiler sin intermediación, gimnasios, alquiler sin intermediación, palenques para la presentación de espectáculos como peleas de gallos, alquiler, salas de conciertos, alquiler sin intermediación, teatros, alquiler sin intermediación	t	\N	\N
769	Alquiler sin intermediación de edificios industriales dentro de un parque industrial	bodegas de autoalmacén dentro de un parque industrial, alquiler sin intermediación, bodegas dentro de un parque industrial, alquiler sin intermediación, bodegas industriales dentro de un parque industrial, alquiler sin intermediación, centros de distribución dentro de un parque industrial, alquiler sin intermediación, centros logísticos dentro de un parque industrial, alquiler sin intermediación, edificios industriales dentro de un parque industrial, alquiler sin intermediación, fabricas dentro 	t	\N	\N
770	Alquiler sin intermediación de otros bienes raíces	bodegas de autoalmacén fuera de un parque industrial, alquiler sin intermediación, bodegas fuera de un parque industrial, alquiler sin intermediación, bodegas industriales fuera de un parque industrial, alquiler sin intermediación, centros de distribución fuera de un parque industrial, alquiler sin intermediación, centros logísticos fuera de un parque industrial, alquiler sin intermediación, edificios industriales fuera de un parque industrial, alquiler sin intermediación, espacios de producción	t	\N	\N
771	Inmobiliarias y corredores de bienes raíces	bienes raíces, corretaje (comercialización) para el alquiler o venta de, corredores de bienes raíces, inmobiliarias, servicios de, intermediación de operaciones inmobiliarias relacionadas con bienes raíces ubicados en desarrollos turísticos, del tipo vivienda turística, multipropiedad y de otro tipo, intermediación en las operaciones de venta y alquiler de bodegas propiedad de terceros, intermediación en las operaciones de venta y alquiler de casas propiedad de terceros, intermediación en las op	t	\N	\N
772	Servicios de administración de bienes raíces	administración de bienes raíces ubicados en desarrollos turísticos, del tipo vivienda turística, multipropiedad y de otro tipo, bienes raíces, administración, edificios comerciales y de servicios, administración, inmuebles no residenciales, administración, inmuebles residenciales, administración, mercados públicos, administración, plazas y centros comerciales, administración, terrenos, administración	t	\N	\N
773	Otros servicios relacionados con los servicios inmobiliarios	bienes raíces agropecuarios, valuación, consultoría de bienes raíces de desarrollos turísticos del tipo vivienda turística, multipropiedad y de otro tipo, consultoría inmobiliaria, departamentos, valuación, inmuebles no residenciales, valuación, inmuebles residenciales, valuación, naves industriales, valuación, peritaje en bienes raíces, promoción de bienes raíces de desarrollos turísticos del tipo vivienda turística, multipropiedad y de otro tipo, promoción inmobiliaria, remate de bienes raíces	t	\N	\N
774	Alquiler de automóviles sin chofer	alquiler de automóviles sin chofer en combinación con el arrendamiento financiero, automóviles sin chofer, alquiler, camionetas sin chofer, alquiler, carrozas sin chofer, alquiler, carruajes sin chofer, alquiler, limusinas sin chofer, alquiler, minivans sin chofer, alquiler	t	\N	\N
829	Otros servicios profesionales, científicos y técnicos	análisis de la letra, antigüedades, valuación, bienes muebles, valuación, embarcaciones marítimas, valuación, grafología, servicios de, inspección de ductos, joyas, valuación, metales, valuación, obras de arte, valuación, piedras preciosas, valuación, servicios meteorológicos	t	\N	\N
775	Alquiler de camiones de carga sin chofer	alquiler de camiones de carga sin chofer en combinación con el arrendamiento financiero, alquiler de tractocamiones sin chofer en combinación con el arrendamiento financiero, alquiler de tráileres sin chofer en combinación con el arrendamiento financiero, camiones de carga sin chofer, alquiler, tractocamiones sin chofer, alquiler, tráileres sin chofer, alquiler	t	\N	\N
776	Alquiler de autobuses, minibuses y remolques sin chofer	alquiler de autobuses sin chofer en combinación con el arrendamiento financiero, alquiler de microbuses sin chofer en combinación con el arrendamiento financiero, alquiler de minibuses sin chofer en combinación con el arrendamiento financiero, alquiler de remolques sin chofer en combinación con el arrendamiento financiero, autobuses sin chofer, alquiler, campers sin chofer, alquiler, casas rodantes no establecidas en un sitio para ser ocupadas como viviendas, alquiler, microbuses sin chofer, alq	t	\N	\N
777	Alquiler de aparatos eléctricos y electrónicos para el hogar y personales	aparatos eléctricos y electrónicos para el hogar, alquiler, aparatos eléctricos y electrónicos personales, alquiler, aparatos electrodomésticos y de línea blanca para el hogar, alquiler, calefactores para el hogar, alquiler, cámaras de video para el hogar, alquiler, equipo de aire acondicionado para el hogar, alquiler, equipo para la distribución de programas por suscripción para el hogar, alquiler de, equipo, componentes y accesorios de sonido para el hogar, alquiler, equipo, componentes y acce	t	\N	\N
778	Alquiler de prendas de vestir	abrigos de piel, alquiler, accesorios de vestir, alquiler de, birretes, alquiler, disfraces, alquiler de, prendas de vestir, alquiler, ropa de cóctel, alquiler, ropa de etiqueta y accesorios para caballero, alquiler, sacos de vestir, alquiler, togas, alquiler, trajes de media etiqueta, alquiler, trajes de primera comunión, alquiler, trajes y vestidos de etiqueta, alquiler, trajes, alquiler, vestidos de noche, alquiler, vestidos de novia, alquiler, vestidos de quince años, alquiler, vestuario art	t	\N	\N
779	Alquiler de mesas, sillas, vajillas y similares	baterías de cocina para ocasiones especiales, alquiler, carpas para ocasiones especiales, alquiler, cristalería para ocasiones especiales, alquiler, cubiertos para ocasiones especiales, alquiler, equipo para ocasiones especiales, alquiler, estrados para ocasiones especiales, alquiler, lonas para ocasiones especiales, alquiler, mantelería para ocasiones especiales, alquiler, mesas para ocasiones especiales, alquiler, servilletas para ocasiones especiales, alquiler, sillas para ocasiones especiale	t	\N	\N
780	Alquiler de otros artículos para el hogar y personales	accesorios para el hogar, alquiler, bananas, alquiler, bastones ortopédicos, alquiler, bicicletas, alquiler, camas médicas de uso doméstico, alquiler, carros de golf, alquiler, casetes de juegos de video, alquiler, casetes musicales, alquiler, cerraduras, sistemas de seguridad, cajas fuertes y otros equipos de seguridad para el hogar, alquiler de, collares ortopédicos, alquiler, corsés ortopédicos, alquiler, discos Blu-ray, alquiler, discos compactos (CD), alquiler, discos de acetato, alquiler, 	t	\N	\N
781	Centros generales de alquiler	artículos de oficina, alquiler no especializado, artículos para el hogar y personales, alquiler no especializado, centros generales de alquiler, servicios de	t	\N	\N
782	Alquiler de maquinaria y equipo para construcción, minería y actividades forestales	alquiler de maquinaria y equipo para la construcción sin operador en combinación con el arrendamiento financiero, alquiler de maquinaria y equipo para la minería sin operador en combinación con el arrendamiento financiero, alquiler de maquinaria y equipo para las actividades forestales sin operador en combinación con el arrendamiento financiero, barrenadoras, alquiler, cimbra de madera, alquiler, cimbra metálica, alquiler, demoledoras, alquiler, equipo de compactación y apuntalamiento, alquiler,	t	\N	\N
783	Alquiler de equipo de transporte, excepto terrestre	aeronaves sin operador, alquiler, alquiler de equipo de transporte sin operador (excepto terrestre) en combinación con el arrendamiento financiero, carros ferroviarios sin operador, alquiler, equipo de transporte excepto terrestre sin operador, alquiler, equipo de transporte por agua, alquiler, trenes sin operador, alquiler	t	\N	\N
784	Alquiler de equipo de cómputo y de otras máquinas y mobiliario de oficina	alquiler de equipo de cómputo y de otras máquinas y mobiliario de oficina en combinación con el arrendamiento financiero, cajas registradoras, alquiler, calculadoras, alquiler, equipo de cómputo, alquiler, equipo electrónico para procesamiento informático, alquiler, equipo periférico, alquiler, fotocopiadoras, alquiler, impresoras, alquiler, máquinas de escribir electrónicas, alquiler, máquinas de escribir no electrónicas, alquiler, mobiliario y equipo de oficina, alquiler	t	\N	\N
785	Alquiler de maquinaria y equipo agropecuario, pesquero y para la industria manufacturera	alquiler de maquinaria y equipo agropecuario, pesquero y para la industria manufacturera sin operador en combinación con el arrendamiento financiero, arados, alquiler, aspersores, alquiler, bebederos, alquiler, bombas, alquiler, calderas, alquiler, cortadoras, alquiler, cosechadoras, alquiler, cribadoras para la agricultura, alquiler, cuchillas, alquiler, desmenuzadoras, alquiler, equipo de generación y transmisión de energía eléctrica, alquiler, extintores, alquiler, incubadoras, alquiler, maqu	t	\N	\N
786	Alquiler de maquinaria y equipo para mover, levantar y acomodar materiales	alquiler de maquinaria y equipo para mover, levantar y acomodar materiales en combinación con el arrendamiento financiero, andamios, alquiler, aparejos, alquiler, cargadores frontales, alquiler, carretillas, alquiler, carretones, alquiler, diablos de carga, alquiler, elevadores, alquiler, gatos hidráulicos, alquiler, grúas para usos diferentes a la construcción, alquiler, malacates, alquiler, maquinaria y equipo para mover, levantar y acomodar materiales, alquiler, montacargas, alquiler, platafo	t	\N	\N
787	Alquiler de maquinaria y equipo comercial y de servicios	alquiler de maquinaria y equipo comercial y de servicios en combinación con el arrendamiento financiero, amplificadores, alquiler, anaqueles para el comercio y los servicios, alquiler, bafles, alquiler, básculas para el comercio y los servicios, alquiler, canastillas de autoservicio, alquiler, carros de autoservicio, alquiler, cerraduras, sistemas de seguridad, cajas fuertes y otros equipos de seguridad para uso no residencial, alquiler de, congeladores para el comercio y los servicios, alquiler	t	\N	\N
788	Servicios de alquiler de marcas registradas, patentes y franquicias	derechos para exploración o explotación de recursos naturales, alquiler, franquicias, alquiler, licenciamiento de derechos para el uso de invenciones protegidas por patentes, licenciamiento de derechos para el uso de marcas registradas, licencias, alquiler, marcas registradas, alquiler, nombres comerciales, alquiler, patentes, alquiler	t	\N	\N
921	Consultorios de psicología del sector privado	consulta psicológica en consultorios del sector privado, cursos de equilibrio emocional en consultorios del sector privado, psicología en consultorios del sector privado, terapias de psicología clínica en consultorios del sector privado, terapias de psicología educativa en consultorios del sector privado, terapias de psicología industrial en consultorios del sector privado	t	\N	\N
789	Bufetes jurídicos	adopciones, tramitación, amparos, tramitación, asuntos sindicales, servicios de abogados especializados en, bufetes jurídicos, consultoría legal en materia de jubilaciones, consultoría legal en materia de negligencia civil, consultoría legal en materia de propiedad de bienes raíces, derecho administrativo, consultoría, derecho civil, consultoría, derecho corporativo, consultoría, derecho familiar, consultoría, derecho fiscal, consultoría, derecho internacional, consultoría, derecho laboral, cons	t	\N	\N
790	Notarías públicas	cartas poder, elaboración, cartas tutelares, elaboración, certificación de adjudicaciones en actos extrajudiciales, certificación de hechos, certificación de la identidad de personas, contratos de arrendamiento, elaboración, contratos de compraventa, elaboración, corredores públicos, servicios de, correduría pública, escrituras, elaboración, notarías públicas, servicios de, notarios públicos, servicios de, poderes notariales, elaboración, testamentos, elaboración, validación y ratificación de fi	t	\N	\N
791	Servicios de apoyo para efectuar trámites legales	apoyo en el registro de títulos de propiedad prestados por unidades económicas que no son notarías, apoyo para arreglo de documentos de compra y venta de bienes, apoyo para efectuar trámites legales, asesoría para efectuar trámites legales, búsqueda, llenado y presentación de documentos legales, entrega de citatorios, investigación de cumplimiento de requisitos legales para la venta de inmuebles, notificación, servicios de, registros de derechos de autor, tramitación, registros de marcas comerci	t	\N	\N
792	Servicios de contabilidad y auditoría	acuerdos sobre procedimientos para la revisión de información financiera, auditoría de cuentas financieras específicas, auditoría de estados financieros, auditoría fiscal, servicios de, auditoría, servicios de, compromisos de revisión de estados financieros, consultoría contable, consultoría en impuestos para personas físicas, consultoría en impuestos para personas morales, consultoría fiscal, contabilidad general excluyendo el cálculo de nómina, contabilidad general y cálculo de nómina, despach	t	\N	\N
793	Otros servicios técnicos relacionados con la contabilidad	cálculo de impuestos, cálculo de saldo a favor, consultoría en la interpretación de las leyes tributarias, contabilidad, servicios técnicos de, formatos fiscales, llenado, formatos para declaración de impuestos y pago de derechos, llenado, formatos para solicitud de devolución de impuestos, llenado, nóminas, elaboración, reportes de nómina a petición del cliente, elaboración	t	\N	\N
794	Servicios de arquitectura	anteproyectos arquitectónicos, arquitectura, consultoría, arquitectura, servicios de, diseño arquitectónico de edificaciones, edificaciones no residenciales, diseño arquitectónico, edificaciones no residenciales, planeación, edificaciones residenciales, diseño arquitectónico, edificaciones residenciales, planeación, inmuebles industriales, proyectos arquitectónicos, inmuebles para comercios y restaurantes, proyectos arquitectónicos, inmuebles para el alojamiento, proyectos arquitectónicos, inmue	t	\N	\N
795	Servicios de arquitectura de paisaje y urbanismo	áreas residenciales, diseño de proyectos de arquitectura de paisaje, arquitectura de paisaje para accesibilidad a un lugar, diseño de proyectos, arquitectura de paisaje para la preparación y modificación del terreno, diseño de proyectos, arquitectura de paisaje y urbanismo, diseño, arquitectura de paisaje, consultoría, arquitectura de paisaje, diseño, caminos, diseño de proyectos de arquitectura de paisaje, campos de golf, diseño de proyectos de arquitectura de paisaje, centros comerciales, dise	t	\N	\N
796	Servicios de ingeniería	ingeniería acústica, consultoría, ingeniería acústica, diseño de proyectos, ingeniería alimentaria, consultoría, ingeniería alimentaria, diseño de proyectos, ingeniería ambiental, diseño de proyectos, ingeniería astronáutica, consultoría, ingeniería astronáutica, diseño de proyectos, ingeniería civil, consultoría, ingeniería civil, diseño de proyectos, ingeniería de agua potable, diseño de proyectos, ingeniería de alcantarillado, diseño de proyectos, ingeniería de autopistas y carreteras, diseño	t	\N	\N
797	Servicios de dibujo	circuitos electrónicos, dibujo, componentes estructurales para proyectos de edificación, dibujo de, componentes estructurales para proyectos de ingeniería civil, dibujo de, diagramas de flujo de procesos industriales, dibujo de, dibujo de diseño de paisaje, dibujo de diseño interior, dibujo del sitio para proyectos de ingeniería civil, dibujo, consultoría, dibujo, servicios de, dibujos arquitectónicos, dibujos detallados para la fabricación de cortes de acero, dibujos para presentaciones, dibujo	t	\N	\N
798	Servicios de inspección de edificios	asbestos, inspección, calidad del agua, inspección, calidad del aire dentro de inmuebles, inspección, casas, inspección, construcción de casas nuevas, inspección, detección de riesgos ambientales en edificaciones no residenciales, detección de riesgos ambientales en edificaciones residenciales, dióxido o monóxido de carbón, inspección, edificios comerciales, inspección, edificios en proceso de construcción, inspección, edificios ya construidos, inspección, estructura de obras ya construidas, ins	t	\N	\N
799	Servicios de levantamiento geofísico	datos geofísicos por métodos aéreos, adquisición, datos geofísicos por métodos aéreos, adquisición y procesamiento, datos geofísicos por métodos aéreos, interpretación, datos geofísicos por métodos aéreos, procesamiento, datos geofísicos por métodos aéreos, procesamiento e interpretación, datos geofísicos por métodos aéreos; adquisición, procesamiento e interpretación, datos geofísicos por métodos no sísmicos desde el mar, adquisición, datos geofísicos por métodos no sísmicos desde el mar, adqui	t	\N	\N
800	Servicios de elaboración de mapas	aerotriangulación, servicios de, agrimensura, servicios de, apoyo terrestre, servicios de, batimetrías, servicios de, capacitación relacionada al levantamiento de mapas, cartas aeronáuticas, elaboración, cartas náuticas, elaboración, consultoría geoespacial, conversión de datos geoespaciales, datos geoespaciales, interpretación, desarrollo de sistemas de información geográfica a petición del cliente, digitalización de datos geoespaciales, fotografías e imágenes geoespaciales aéreas, obtención, f	t	\N	\N
801	Servicios de laboratorios de pruebas	certificación de productos, consultoría en pruebas a productos o sustancias, instrumentos y materiales de referencia, calibración, laboratorios de pruebas a productos o sustancias, servicios de, peritaje en pruebas a productos o sustancias, productos que se comercializan, inspección de, pruebas a la calidad del aire, servicios de, pruebas a las bebidas, servicios de, pruebas a los alimentos, servicios de, pruebas a los minerales, servicios de, pruebas a los residuos tóxicos, servicios de, prueba	t	\N	\N
922	Consultorios de psicología del sector público	consulta psicológica en consultorios del sector público, cursos de equilibrio emocional en consultorios del sector público, psicología en consultorios del sector público, terapias de psicología clínica en consultorios del sector público, terapias de psicología educativa en consultorios del sector público, terapias de psicología industrial en consultorios del sector público	t	\N	\N
802	Diseño y decoración de interiores	decoración de interiores, diseño de espacios interiores, consultoría, diseño de interiores, edificaciones históricas, diseño de espacios interiores, edificaciones no residenciales, decoración de espacios interiores, edificaciones no residenciales, diseño de espacios interiores, edificaciones no residenciales, planeación de espacios interiores, edificaciones residenciales, decoración de espacios interiores, edificaciones residenciales, diseño de espacios interiores, edificaciones residenciales, p	t	\N	\N
803	Diseño industrial	artículos personales y para el hogar, diseño industrial, automóviles, diseño industrial, camiones, diseño industrial, contenedores, diseño industrial, diseño industrial y fabricación de modelos o prototipos, diseño industrial, consultoría, empaques, diseño industrial, envases, diseño industrial, equipo de cómputo, diseño industrial, equipo de transporte, diseño industrial, herramientas, diseño industrial, maquinaria y equipo para la industria alimentaria, diseño industrial, maquinaria y equipo p	t	\N	\N
804	Diseño gráfico	artistas dedicados a generar dibujos e ilustraciones, discos, diseño gráfico de, diseño gráfico, diseño gráfico comercial, diseño gráfico corporativo, diseño gráfico de títulos para programas de televisión, películas y audiovisuales, diseño gráfico editorial, diseño gráfico publicitario, diseño gráfico, consultoría, envases y empaques, diseño gráfico, folletos, diseño gráfico, ilustraciones, diseño gráfico, libros, diseño gráfico, logotipos y marcas, diseño gráfico, páginas de internet, diseño g	t	\N	\N
805	Diseño de modas y otros diseños especializados	accesorios de vestir, diseño, calzado, diseño, creación y desarrollo de productos de moda, diseño de modas, joyas, diseño, ropa, diseño, textil, diseño	t	\N	\N
806	Servicios de diseño de sistemas de cómputo y servicios relacionados	administración de centros de cómputo, análisis de datos, aplicaciones móviles (apps), diseño y desarrollo de, bases de datos, diseño y desarrollo de, diseño, desarrollo e integración de aplicaciones hechas a la medida del cliente sobre un software empaquetado de aplicación de mercados verticales, diseño, desarrollo e integración de aplicaciones hechas a la medida del cliente sobre un software empaquetado de aplicación general, instalación de equipo y redes informáticas, consultoría, nuevas aplic	t	\N	\N
807	Servicios de consultoría en administración	administración de la producción, consultoría, administración de operaciones y de la cadena de suministro, consultoría, administración de recursos humanos, consultoría, administración de servicios públicos, consultoría, administración estratégica de negocios, consultoría, administración financiera, consultoría, administración general, consultoría, administración organizacional, consultoría, certificación de sistemas administrativos, certificaciones de calidad, consultoría actuarial, consultoría e	t	\N	\N
808	Servicios de consultoría en medio ambiente	auditoría ambiental del agua, auditoría ambiental del aire, auditoría ambiental del ruido, auditoría ambiental del suelo, auditoría ambiental integrada (agua, aire, ruido y suelo), servicios de, consultoría para la elaboración de políticas ambientales, contaminación de asbestos, consultoría, control de la contaminación, consultoría, estudios de desarrollo ecológico sustentable, elaboración, estudios de impacto ambiental al agua, elaboración, estudios de impacto ambiental al aire, elaboración, es	t	\N	\N
809	Otros servicios de consultoría científica y técnica	agricultura, consultoría, análisis de riesgos, consultoría, aprovechamiento forestal, pesca y caza; consultoría, biología, consultoría, comercio exterior, consultoría, consultoría patrimonial, control de calidad, consultoría, cría y explotación de animales, consultoría, desarrollo industrial, consultoría, desarrollos turísticos, consultoría, economía, consultoría, energía, consultoría, estadística, consultoría, física, consultoría, geofísica, consultoría, geología, consultoría, hidrología, consu	t	\N	\N
810	Servicios de investigación científica y desarrollo en ciencias naturales y exactas, ingeniería, y ciencias de la vida, prestados por el sector privado	centros del sector privado de investigación científica y desarrollo en biología, servicios de, centros del sector privado de investigación científica y desarrollo en biotecnología, servicios de, centros del sector privado de investigación científica y desarrollo en ciencias de la vida, servicios de, centros del sector privado de investigación científica y desarrollo en ciencias físicas, servicios de, investigación científica y desarrollo en acústica y óptica, servicios del sector privado, invest	t	\N	\N
811	Servicios de investigación científica y desarrollo en ciencias naturales y exactas, ingeniería, y ciencias de la vida, prestados por el sector público	centros del sector público de investigación científica y desarrollo en biología, servicios de, centros del sector público de investigación científica y desarrollo en biotecnología, servicios de, centros del sector público de investigación científica y desarrollo en ciencias de la vida, servicios de, centros del sector público de investigación científica y desarrollo en ciencias físicas, servicios de, investigación científica y desarrollo en acústica y óptica, servicios del sector público, invest	t	\N	\N
812	Servicios de investigación científica y desarrollo en ciencias sociales y humanidades, prestados por el sector privado	centros del sector privado de investigación científica y desarrollo en ciencias sociales, servicios de, centros del sector privado de investigación científica y desarrollo en humanidades, servicios de, investigación científica y desarrollo en administración y comercio, servicios del sector privado, investigación científica y desarrollo en antropología, servicios del sector privado, investigación científica y desarrollo en arqueología, servicios del sector privado, investigación científica y desa	t	\N	\N
813	Servicios de investigación científica y desarrollo en ciencias sociales y humanidades, prestados por el sector público	centros del sector público de investigación científica y desarrollo en ciencias sociales, servicios de, centros del sector público de investigación científica y desarrollo en humanidades, servicios de, investigación científica y desarrollo en administración y comercio, servicios del sector público, investigación científica y desarrollo en antropología, servicios del sector público, investigación científica y desarrollo en arqueología, servicios del sector público, investigación científica y desa	t	\N	\N
814	Agencias de publicidad	agencias de promoción de ventas, agencias de publicidad, colocación de anuncios publicitarios por agencias de publicidad con servicios integrados, comunicación y mercadotecnia, servicio integral de, creación de campañas publicitarias y difusión en medios de comunicación, decoración de exhibidores por agencias de publicidad con servicios integrados, diseño de anuncios publicitarios por agencias de publicidad con servicios integrados, diseño de campañas publicitarias por agencias de publicidad con	t	\N	\N
815	Agencias de relaciones públicas	agencias de relaciones públicas, cabildeo, servicios de, capacitación en medios publicitarios, diseño e implementación de campañas para promover la imagen de empresas o de particulares, espacios editoriales, servicios de, manejo de crisis, servicios de, monitoreo y análisis de medios publicitarios, organización de eventos para la recaudación de fondos por agencias de relaciones públicas, política, consultoría, relaciones públicas, consultoría, servicio completo de relaciones públicas de promoció	t	\N	\N
816	Agencias de compra de medios a petición del cliente	agencias de compra de medios a petición del cliente, análisis de la publicidad de la competencia, compra de espacio publicitario en los medios en nombre de publicistas o agencias de publicidad, compra de tiempo publicitario en los medios en nombre de publicistas o agencias de publicidad, elaboración de plan de medios publicitarios, investigación, análisis y verificación de medios publicitarios, planeación y compra de medios publicitarios	t	\N	\N
817	Agencias de representación de medios	agencias de representación de medios, representación de la radio para la venta de tiempo publicitario, representación de la televisión para la venta de tiempo y espacio publicitario, representación de medios impresos para la venta de espacios publicitarios, representación de medios masivos de comunicación para la venta de tiempo y espacio publicitario	t	\N	\N
818	Agencias de anuncios publicitarios	agencias de anuncios publicitarios, anuncios pintados, diseño de, carteles publicitarios, diseño de, colocación y diseño de anuncios publicitarios (con la subcontratación de otra unidad económica para que los fabrique), diseño de anuncios eléctricos, espacios publicitarios en áreas comunes de estaciones de tránsito, renta, espacios publicitarios en exhibidores de gran formato, renta, espacios publicitarios en medios de transporte, renta, espacios publicitarios en mobiliario urbano, renta, espaci	t	\N	\N
819	Agencias de correo directo	adecuación de listas de envío por correo directo, agencias de correo directo, armado y envío de paquetes utilizando las listas del público objetivo, campañas de publicidad por correo directo, depuración de listas de envío por correo directo, diseño y ejecución de campañas publicitarias por correo directo en combinación con la compilación, mantenimiento, renta y venta de listas de clientes potenciales, elaboración del concepto para una campaña de publicidad de correo directo, preparación y envío 	t	\N	\N
820	Distribución de material publicitario	catálogos publicitarios en parabrisas de automóviles, distribución, catálogos publicitarios en tiendas, distribución, catálogos publicitarios puerta por puerta, distribución, cupones publicitarios puerta por puerta, distribución, folletos publicitarios en parabrisas de automóviles, distribución, folletos publicitarios en tiendas, distribución, folletos publicitarios puerta por puerta, distribución, material publicitario en sitios públicos, distribución, muestras publicitarias en tiendas, distrib	t	\N	\N
821	Servicios de rotulación y otros servicios de publicidad	aparadores, decoración, coordinación de la producción y entrega de premios y artículos de publicidad, demostración de productos, escenarios, decoración, exhibidores, decoración, maniquíes, decoración, organización de bienvenidas, perifoneo, servicios de, rotulación, servicios de	t	\N	\N
822	Servicios de investigación de mercados y encuestas de opinión pública	análisis de gustos y preferencias, análisis de impactos publicitarios, análisis y generación de resultados para encuestas de opinión pública, diseño muestral para investigación de mercados y encuestas de opinión pública, encuestas de gustos y preferencias, encuestas de impacto publicitario, encuestas de opinión pública, encuestas de opinión pública en paquete (diseño muestral, levantamiento de información, procesamiento, análisis y generación de resultados), estudios sobre hábitos de compra, ser	t	\N	\N
823	Servicios de fotografía y videograbación	estudios fotográficos, servicios de, fotografía de retratos escolares, fotografía de retratos familiares y personales, fotografía de retratos para identificación, fotografía médica, fotografía para bodas y eventos especiales, fotografía para convenciones, reuniones y eventos empresariales, fotografía para el comercio, fotografía para la industria, fotografía para pasaportes, fotografía por computadora, fotografía publicitaria, fotografía y videograbación para bodas y eventos especiales, fotograf	t	\N	\N
824	Servicios de traducción e interpretación	documentos legales, traducción de, guiones, traducción de, interpretación de lenguaje verbal, interpretación de un idioma a otro, interpretación por señas, peritaje en traducción, traducción de textos, traducción simultánea oral	t	\N	\N
825	Servicios veterinarios para mascotas prestados por el sector privado	bancos de sangre del sector privado para mascotas, servicios, citología clínica para mascotas en laboratorios veterinarios del sector privado, consulta médica veterinaria para mascotas, servicios del sector privado, consultorios médicos veterinarios para mascotas pertenecientes al sector privado, diagnóstico clínico y patológico para mascotas, servicios del sector privado, esterilización de mascotas, servicios del sector privado, hemogramas para mascotas en laboratorios veterinarios del sector p	t	\N	\N
826	Servicios veterinarios para mascotas prestados por el sector público	bancos de sangre del sector público para mascotas, servicios, centros antirrábicos, servicios del sector público, citología clínica para mascotas en laboratorios veterinarios del sector público, consulta médica veterinaria para mascotas, servicios del sector público, consultorios médicos veterinarios para mascotas pertenecientes al sector público, diagnóstico clínico y patológico para mascotas, servicios del sector público, esterilización de mascotas, servicios del sector público, hemogramas par	t	\N	\N
827	Servicios veterinarios para la ganadería prestados por el sector privado	citología clínica para ganado en laboratorios veterinarios del sector privado, consulta médica veterinaria para la ganadería, servicios del sector privado, consultorios médicos veterinarios para ganado pertenecientes al sector privado, diagnóstico clínico y patológico para ganado, servicios del sector privado, esterilización de ganado, servicios del sector privado, hemogramas para ganado en laboratorios veterinarios del sector privado, histopatología para ganado en laboratorios veterinarios del 	t	\N	\N
828	Servicios veterinarios para la ganadería prestados por el sector público	citología clínica para ganado en laboratorios veterinarios del sector público, consulta médica veterinaria para la ganadería, servicios del sector público, consultorios médicos veterinarios para ganado pertenecientes al sector público, diagnóstico clínico y patológico para ganado, servicios del sector público, esterilización de ganado, servicios del sector público, hemogramas para ganado en laboratorios veterinarios del sector público, histopatología para ganado en laboratorios veterinarios del 	t	\N	\N
830	Dirección y administración de grupos empresariales o corporativos	dirección y administración de corporativos, dirección y administración de corporativos bancarios, dirección y administración de corporativos de empresas aseguradoras, dirección y administración de corporativos financieros, dirección y administración de corporativos no financieros, dirección y administración de grupos empresariales, dirección y administración de sociedades de control, tenedoras de acciones que dirigen y controlan otras compañías del mismo grupo	t	\N	\N
831	Tenedoras de acciones	tenedoras de acciones que no dirigen y controlan otras compañías del mismo grupo, teneduría de acciones de empresas financieras, teneduría de acciones de empresas no financieras	t	\N	\N
832	Servicios de administración de negocios	administración especializada de negocios, administración general de negocios	t	\N	\N
833	Servicios integrales de apoyo a los negocios en instalaciones	gestión delegada de operaciones y servicios generales (facilities management) en centros comerciales, gestión delegada de operaciones y servicios generales (facilities management) en edificios de oficinas, gestión delegada de operaciones y servicios generales (facilities management) en hospitales y centros médicos, gestión delegada de operaciones y servicios generales (facilities management) en plantas industriales, instalaciones penitenciarias, operación de, servicios integrales de apoyo a los 	t	\N	\N
834	Agencias de colocación	agencias de colocación, agencias de colocación de personal doméstico, agencias de empleo de artistas, asesoramiento de desvinculación asistida (outplacement) o de cambio de empleo, bolsa de trabajo, servicios de, colocación de personal, consultoría en búsqueda de ejecutivos, contratación de servicios de personal independiente, estudios socioeconómicos por agencias de colocación, servicios de, evaluación de empleados por agencias de colocación, listados de currículum vítae en línea, servicios de,	t	\N	\N
835	Agencias de empleo temporal	administración en el sitio de personal temporal suministrado, agencias de contratación de personal temporal, agencias de empleo temporal, agencias de modelos, agentes de modelos, servicios de, estudios socioeconómicos por agencias de empleo temporal, servicios de, evaluación de empleados por agencias de empleo temporal, meseros para eventos sociales, servicios de, personal secretarial temporal, servicios de, personal temporal de apoyo para oficina, servicios de, suministro de personal temporal, 	t	\N	\N
836	Suministro de personal permanente	administradoras de personal, suministro de empleados y obreros permanentes, suministro de personal a largo plazo, suministro de personal permanente	t	\N	\N
837	Servicios de preparación de documentos	captura de textos, corrección de estilo, estenografía no realizada en los tribunales, formateo de textos, mecanografía, servicios de, preparación de documentos, procesamiento y edición de textos	t	\N	\N
838	Servicios de casetas telefónicas	casetas telefónicas (sin operar redes telefónicas alámbricas), servicios de, casetas telefónicas rurales (sin operar redes telefónicas alámbricas), servicios de	t	\N	\N
839	Servicios de recepción de llamadas telefónicas y promoción por teléfono	centros de atención telefónica (call centers), servicios de, centros de contacto (contact centers), servicios de, correo de voz, servicios de, llamadas salientes, servicios de, marcaje de llamadas sin operar las redes, mercadeo telefónico por medio de llamadas entrantes, servicios de, mercadeo telefónico por medio de llamadas salientes, servicios de, promoción por teléfono de bienes o servicios, recepción de llamadas telefónicas en nombre de los clientes, servicios telefónicos de atención al cli	t	\N	\N
840	Servicios de fotocopiado, fax y afines	ampliación de fotocopias de textos, centros de fotocopiado, encuadernación en centros de fotocopiado, servicios de, engargolado, servicios de, enmicado, servicios de, envío masivo de fax, fax, servicios de, fotocopiado, servicios de, recepción de correspondencia, reducción de fotocopias	t	\N	\N
841	Servicios de acceso a computadoras	acceso a computadoras, servicios de, café internet, servicios de, cibercafé, servicios de, internet público, servicios de	t	\N	\N
842	Agencias de cobranza	agencias de cobranza, carteras vencidas, recuperación de, cobranza, servicios de, cobro de deudas en nombre del cliente, deudas de los individuos, recuperación de, deudas de los negocios, recuperación de	t	\N	\N
843	Despachos de investigación de solvencia financiera	buró de crédito, despachos de investigación de solvencia financiera, investigación crediticia, investigación de riesgo financiero de los gobiernos, investigación de solvencia comercial, investigación de solvencia crediticia, investigación de solvencia financiera	t	\N	\N
844	Otros servicios de apoyo secretarial y similares	apartados postales del sector privado, servicios de, códigos de barras, expedición, doblaje, traducción y transcripción simultánea de subtítulos en tiempo real, embargo de bienes, servicios de, estenografía realizada en los tribunales, organización y asistencia de teleconferencias, realización de pagos en nombre de terceros que no implican ningún trámite legal, transcripción simultánea de diálogos para la televisión, en reuniones y conferencias	t	\N	\N
845	Agencias de viajes	agencias de viajes, asesoría, planeación y organización de itinerarios de viajes	t	\N	\N
846	Organización de excursiones y paquetes turísticos para agencias de viajes (Operadores de tours)	operadores de tours, servicios de, operadores mayoristas de viajes, servicios de, organización de excursiones y paquetes turísticos para ser vendidos por agencias de viajes, organización de paquetes turísticos prearmados, reventa de paquetes turísticos prearmados	t	\N	\N
847	Otros servicios de reservaciones	diseño, implementación y coordinación integral de un conjunto de servicios dentro de un destino turístico, intercambio de tiempos compartidos (promoción y comercialización, administración, edición y envío de directorios), promoción de ciudades con infraestructura para realizar congresos, conferencias, ferias y seminarios, reservación de boletos para espectáculos, reservación de habitaciones en hoteles, reservación de lugares en líneas de transporte, reservación de lugares en restaurantes, reserv	t	\N	\N
848	Servicios de investigación y de protección y custodia, excepto mediante monitoreo	atención a cajeros automáticos (dotación de efectivo, corte y arqueo de caja, aprovisionamiento de papelería, etc.), detección de mentiras, detectives privados, servicios de, empaquetado de dinero, encartuchado de monedas y fajillas de billetes, escoltas, servicios de, guardaespaldas, servicios de, guardias, servicios de, investigaciones empresariales y laborales, investigaciones legales, investigaciones para seguros, investigaciones personales y familiares, nóminas, ensobretado, perros guardian	t	\N	\N
923	Consultorios del sector privado de audiología y de terapia ocupacional, física y del lenguaje	audiología en consultorios del sector privado, terapia del lenguaje en consultorios del sector privado, terapia deportiva en consultorios del sector privado, terapia física en consultorios del sector privado, terapia ocupacional en consultorios del sector privado	t	\N	\N
849	Servicios de protección y custodia mediante el monitoreo de sistemas de seguridad	cerraduras de alta seguridad, instalación y reparación, cerrajería de alta seguridad, monitoreo en combinación con la comercialización, instalación y reparación de sistemas de seguridad, protección y custodia mediante el monitoreo de sistemas de seguridad, seguridad electrónica no residencial con monitoreo, servicios de, seguridad electrónica residencial con monitoreo, servicios de, sistemas de alarmas contra incendios, monitoreo, sistemas de alarmas contra robo, monitoreo, sistemas de seguridad	t	\N	\N
850	Servicios de control y exterminación de plagas	fumigación (control y exterminación) de plagas en casas habitación, fumigación (control y exterminación) de plagas en edificios, fumigación (control y exterminación) de plagas en inmuebles no residenciales, fumigación (control y exterminación) de plagas en inmuebles residenciales, fumigación (control y exterminación) de plagas en jardines, fumigación (control y exterminación) de plagas en medios de transporte, fumigación no agrícola, servicios, plagas, control y exterminación	t	\N	\N
851	Servicios de limpieza de inmuebles	aeronaves, aseo interior de, bancos y otras instituciones financieras, limpieza integral en, baños, limpieza, barcos, aseo interior, carros ferroviarios, aseo interior, centros comerciales, limpieza integral en, hospitales y consultorios médicos, limpieza integral en, interiores de inmuebles residenciales, limpieza general en, limpieza postconstrucción o remodelación, oficinas, limpieza de, pisos, encerado, pisos, lavado, plantas industriales, limpieza integral en, trenes, aseo interior de, vidr	t	\N	\N
852	Servicios de instalación y mantenimiento de áreas verdes	adornos en áreas verdes, instalación, andadores en áreas verdes, instalación, áreas verdes en campos de golf, instalación y mantenimiento, áreas verdes en centros comerciales, instalación y mantenimiento, áreas verdes en parques, instalación y mantenimiento, áreas verdes, instalación y mantenimiento, cercas en áreas verdes, instalación, control de hierbas, diseño, cuidado y mantenimiento de áreas verdes en combinación con la construcción de andadores, estanques, adornos, cercas, estanques en áre	t	\N	\N
853	Servicios de limpieza de tapicería, alfombras y muebles	alfombras y tapetes, limpieza en planta, alfombras y tapetes, limpieza no residencial a domicilio, alfombras y tapetes, limpieza residencial a domicilio, limpieza por inundaciones u otros siniestros, muebles, limpieza en planta, muebles, limpieza no residencial a domicilio, muebles, limpieza residencial a domicilio, tapicería, limpieza	t	\N	\N
854	Otros servicios de limpieza	albercas, limpieza, calentadores de agua, limpieza, chimeneas, limpieza, cisternas, limpieza y desinfección, ductos de aire acondicionado, limpieza, ductos de calefacción, limpieza, ductos de sistemas ambientales, limpieza, ductos de ventilación, limpieza, estacionamientos, limpieza de, extractores de aire, limpieza, fachadas de inmuebles, limpieza, filtros industriales, limpieza, hornos, limpieza, incineradores, limpieza, tanques elevados, limpieza, tinacos, limpieza, torres de enfriamiento, li	t	\N	\N
855	Servicios de empacado y etiquetado	bienes propiedad de terceros, empacado, bienes propiedad de terceros, etiquetado, cajas o kits propiedad de terceros, empacado, cosméticos, empacado, empacado, servicios de, enrollado de papel aluminio en tubos de cartón, servicios de, envases y empaques, clasificación, envases y empaques, reempacado, envoltura de regalos, servicios de, etiquetado, servicios de, ropa, empacado	t	\N	\N
856	Organizadores de convenciones y ferias comerciales e industriales	organización de eventos para la recaudación de fondos, organización y promoción de congresos, organización y promoción de convenciones, organización y promoción de ferias comerciales, organización y promoción de ferias industriales	t	\N	\N
857	Otros servicios de apoyo a los negocios	bomberos particulares, servicios de, clasificación de correspondencia, comunicación electrónica entre socios, decoración con globos para eventos sociales, intercambio corporativo (trueque formal o bartering services), servicios de, lectura de medidores de agua, lectura de medidores de electricidad, lectura de medidores de gas, limpieza de pescado a petición de terceros, organización de subastas, programas de lealtad, administración de, selección de cupones	t	\N	\N
858	Recolección de residuos peligrosos por el sector privado	aceites, grasas, mezclas y residuos aceitosos, recolección por el sector privado, baterías usadas, recolección por el sector privado, Bifenilos Policlorados (BPCs), recolección por el sector privado, consolidación, almacenamiento temporal y preparación de residuos peligrosos para el transporte por el sector privado, estaciones de transferencia de residuos peligrosos del sector privado, servicios de, fondos de destilación, recolección por el sector privado, llantas usadas, recolección por el sect	t	\N	\N
859	Recolección de residuos peligrosos por el sector público	aceites, grasas, mezclas y residuos aceitosos, recolección por el sector público, baterías usadas, recolección por el sector público, Bifenilos Policlorados (BPCs), recolección por el sector público, consolidación, almacenamiento temporal y preparación de residuos peligrosos para el transporte por el sector público, estaciones de transferencia de residuos peligrosos del sector público, servicios de, fondos de destilación, recolección por el sector público, llantas usadas, recolección por el sect	t	\N	\N
860	Recolección de residuos no peligrosos por el sector privado	barrido urbano por el sector privado, basura, recolección por el sector privado, consolidación, almacenamiento temporal y preparación de residuos no peligrosos para el transporte por el sector privado, estaciones de transferencia del sector privado de residuos no peligros, servicios de, materiales reciclables no peligrosos, recolección no residencial por el sector privado, materiales reciclables no peligrosos, recolección por el sector privado, materiales reciclables no peligrosos, recolección r	t	\N	\N
861	Recolección de residuos no peligrosos por el sector público	barrido urbano por el sector público, basura, recolección por el sector público, consolidación, almacenamiento temporal y preparación de residuos no peligrosos para el transporte por el sector público, estaciones de transferencia del sector público de residuos no peligros, servicios de, materiales reciclables no peligrosos, recolección no residencial por el sector público, materiales reciclables no peligrosos, recolección por el sector público, materiales reciclables no peligrosos, recolección r	t	\N	\N
862	Tratamiento y disposición final de residuos peligrosos por el sector privado	aceites, grasas, mezclas y residuos aceitosos, tratamiento por el sector privado, baterías usadas, tratamiento por el sector privado, Bifenilos Policlorados (BPCs), tratamiento por el sector privado, confinamientos controlados del sector privado, disposición de residuos peligrosos en, confinamientos en formaciones geológicas estables del sector privado, disposición de residuos peligrosos en, contenedores sobre tierra del sector privado, disposición de residuos peligrosos en, llantas usadas, trat	t	\N	\N
863	Tratamiento y disposición final de residuos peligrosos por el sector público	aceites, grasas, mezclas y residuos aceitosos, tratamiento por el sector público, baterías usadas, tratamiento por el sector público, Bifenilos Policlorados (BPCs), tratamiento por el sector público, confinamientos controlados del sector público, disposición de residuos peligrosos en, confinamientos en formaciones geológicas estables del sector público, disposición de residuos peligrosos en, contenedores sobre tierra del sector público, disposición de residuos peligrosos en, llantas usadas, trat	t	\N	\N
864	Tratamiento y disposición final de residuos no peligrosos por el sector privado	cámaras de combustión para residuos no peligrosos del sector privado, servicios de, rellenos sanitarios del sector privado, disposición de residuos no peligrosos en, residuos no peligrosos, disposición por el sector privado, residuos no peligrosos, incineración por el sector privado, residuos no peligrosos, tratamiento por el sector privado	t	\N	\N
865	Tratamiento y disposición final de residuos no peligrosos por el sector público	cámaras de combustión para residuos no peligrosos del sector público, servicios de, rellenos sanitarios del sector público, disposición de residuos no peligrosos en, residuos no peligrosos, disposición por el sector público, residuos no peligrosos, incineración por el sector público, residuos no peligrosos, tratamiento por el sector público	t	\N	\N
866	Servicios de remediación por el sector privado	construcciones contaminadas por asbestos, remediación por el sector privado, construcciones contaminadas por pintura con plomo, remediación por el sector privado, construcciones contaminadas por radón, remediación por el sector privado, control, contención y monitoreo por el sector privado de sitios contaminados por residuos no peligrosos, control, contención y monitoreo por el sector privado de sitios contaminados por residuos o materiales peligrosos, limpieza del aire por el sector privado en 	t	\N	\N
867	Servicios de remediación por el sector público	construcciones contaminadas por asbestos, remediación por el sector público, construcciones contaminadas por pintura con plomo, remediación por el sector público, construcciones contaminadas por radón, remediación por el sector público, control, contención y monitoreo por el sector público de sitios contaminados por residuos no peligrosos, control, contención y monitoreo por el sector público de sitios contaminados por residuos o materiales peligrosos, limpieza del aire por el sector público en 	t	\N	\N
868	Recuperación de residuos por el sector privado	botellas de PET usadas, clasificación (manejo de residuos no peligrosos) por el sector privado, botellas de PET usadas, recuperación (manejo de residuos no peligrosos) por el sector privado, botellas de PET usadas, selección (manejo de residuos no peligrosos) por el sector privado, cartón usado, clasificación por el sector privado (manejo de residuos no peligrosos), cartón usado, compactación por el sector privado (manejo de residuos no peligrosos), cartón usado, recuperación por el sector priva	t	\N	\N
869	Recuperación de residuos por el sector público	botellas de PET usadas, clasificación (manejo de residuos no peligrosos) por el sector público, botellas de PET usadas, recuperación (manejo de residuos no peligrosos) por el sector público, botellas de PET usadas, selección (manejo de residuos no peligrosos) por el sector público, cartón usado, clasificación por el sector público (manejo de residuos no peligrosos), cartón usado, compactación por el sector público (manejo de residuos no peligrosos), cartón usado, recuperación por el sector públi	t	\N	\N
870	Otros servicios de manejo de residuos por el sector privado	cárcamos, limpieza por el sector privado, documentos o archivos, destrucción por el sector privado (manejo de residuos no peligrosos), fosas sépticas, limpieza y mantenimiento por el sector privado, instalaciones clausuradas de disposición de residuos no peligrosos, mantenimiento por el sector privado, instalaciones clausuradas de disposición de residuos peligrosos, mantenimiento por el sector privado, instalaciones de captación, retención y drenaje de residuos peligrosos, limpieza y mantenimien	t	\N	\N
871	Otros servicios de manejo de residuos por el sector público	cárcamos, limpieza por el sector público, instalaciones clausuradas de disposición de residuos no peligrosos, mantenimiento por el sector público, instalaciones clausuradas de disposición de residuos peligrosos, mantenimiento por el sector público, instalaciones de captación, retención y drenaje de residuos peligrosos, limpieza y mantenimiento por el sector público, instalaciones de disposición de residuos no peligrosos, clausura por el sector público, instalaciones de disposición de residuos pe	t	\N	\N
872	Escuelas de educación preescolar y centros de estimulación temprana del sector privado	centros de estimulación temprana del sector privado, educación preescolar impartida en escuelas del sector privado mediante sistema a distancia, educación preescolar impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación preescolar del sector privado, servicios educativos, jardines de niños del sector privado, servicios educativos	t	\N	\N
873	Escuelas de educación preescolar y centros de estimulación temprana del sector público	centros de estimulación temprana del sector público, educación preescolar impartida en escuelas del sector público mediante sistema a distancia, educación preescolar impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación preescolar comunitaria del sector público, servicios educativos, escuelas de educación preescolar del sector público, servicios educativos, escuelas de educación preescolar indígena del sector público, servicios educativos, escuelas rurales	t	\N	\N
874	Escuelas de educación primaria del sector privado	educación primaria impartida en escuelas del sector privado mediante sistema a distancia, educación primaria impartida en escuelas del sector privado mediante sistema abierto, educación primaria impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación primaria bilingüe-bicultural del sector privado, servicios educativos, escuelas de educación primaria del sector privado con internado, servicios educativos, escuelas de educación primaria del sector privado par	t	\N	\N
875	Escuelas de educación primaria del sector público	educación primaria impartida en escuelas del sector público mediante sistema a distancia, educación primaria impartida en escuelas del sector público mediante sistema abierto, educación primaria impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación primaria comunitaria del sector público, servicios educativos, escuelas de educación primaria del sector público para adultos, servicios educativos, escuelas de educación primaria del sector público, servicios e	t	\N	\N
876	Escuelas de educación secundaria general del sector privado	educación secundaria general impartida en escuelas del sector privado mediante sistema a distancia, educación secundaria general impartida en escuelas del sector privado mediante sistema abierto, educación secundaria general impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación secundaria general del sector privado con horario especial para trabajadores, servicios educativos, escuelas de educación secundaria general del sector privado con internado, servic	t	\N	\N
877	Escuelas de educación secundaria general del sector público	educación secundaria general impartida en escuelas del sector público mediante sistema a distancia, educación secundaria general impartida en escuelas del sector público mediante sistema abierto, educación secundaria general impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación secundaria general comunitaria del sector público, servicios educativos, escuelas de educación secundaria general del sector público con horario especial para trabajadores, servicio	t	\N	\N
878	Escuelas de educación secundaria técnica del sector privado	educación secundaria técnica impartida en escuelas del sector privado mediante sistema a distancia, educación secundaria técnica impartida en escuelas del sector privado mediante sistema abierto, educación secundaria técnica impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación secundaria técnica del sector privado con internado, servicios educativos, escuelas de educación secundaria técnica del sector privado, servicios educativos	t	\N	\N
879	Escuelas de educación secundaria técnica del sector público	educación secundaria técnica impartida en escuelas del sector público mediante sistema a distancia, educación secundaria técnica impartida en escuelas del sector público mediante sistema abierto, educación secundaria técnica impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación secundaria técnica del sector público, servicios educativos, escuelas de educación secundaria técnica indígena del sector público, servicios educativos	t	\N	\N
880	Escuelas de educación media técnica terminal del sector privado	educación media técnica terminal impartida en escuelas del sector privado mediante sistema a distancia, educación media técnica terminal impartida en escuelas del sector privado mediante sistema abierto, educación media técnica terminal impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación media técnica terminal agropecuaria del sector privado, servicios educativos, escuelas de educación media técnica terminal de servicios del sector privado, servicios edu	t	\N	\N
881	Escuelas de educación media técnica terminal del sector público	educación media técnica terminal impartida en escuelas del sector público mediante sistema a distancia, educación media técnica terminal impartida en escuelas del sector público mediante sistema abierto, educación media técnica terminal impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación media técnica terminal agropecuaria del sector público, servicios educativos, escuelas de educación media técnica terminal de servicios del sector público, servicios edu	t	\N	\N
882	Escuelas de educación media superior del sector privado	colegios de ciencias y humanidades del sector privado, servicios educativos, educación media superior impartida en escuelas del sector privado mediante sistema a distancia, educación media superior impartida en escuelas del sector privado mediante sistema abierto, educación media superior impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación de bachillerato general de carácter propedéutico del sector privado, servicios educativos, escuelas de educación de 	t	\N	\N
883	Escuelas de educación media superior del sector público	colegios de bachilleres del sector público, servicios educativos, colegios de ciencias y humanidades del sector público, servicios educativos, educación media superior impartida en escuelas del sector público mediante sistema a distancia, educación media superior impartida en escuelas del sector público mediante sistema abierto, educación media superior impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación de bachillerato general de carácter propedéutico d	t	\N	\N
884	Escuelas del sector privado que combinan diversos niveles de educación	educación correspondiente a dos o más niveles educativos impartida en escuelas del sector privado mediante sistema a distancia, educación correspondiente a dos o más niveles educativos impartida en escuelas del sector privado mediante sistema abierto, educación correspondiente a dos o más niveles educativos impartida en escuelas del sector privado mediante sistema escolarizado, escuelas del sector privado que combinan diversos niveles de educación básica y media y que además proporcionan capacit	t	\N	\N
885	Escuelas del sector público que combinan diversos niveles de educación	educación correspondiente a dos o más niveles educativos impartida en escuelas del sector público mediante sistema a distancia, educación correspondiente a dos o más niveles educativos impartida en escuelas del sector público mediante sistema abierto, educación correspondiente a dos o más niveles educativos impartida en escuelas del sector público mediante sistema escolarizado, escuelas del sector público que combinan diversos niveles de educación básica y media y que además proporcionan capacit	t	\N	\N
886	Escuelas del sector privado de educación para necesidades especiales	educación para necesidades especiales impartida en escuelas del sector privado mediante sistema a distancia, educación para necesidades especiales impartida en escuelas del sector privado mediante sistema abierto, educación para necesidades especiales impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación preescolar del sector privado para necesidades especiales, servicios educativos, escuelas de educación primaria del sector privado para necesidades especi	t	\N	\N
887	Escuelas del sector público de educación para necesidades especiales	educación para necesidades especiales impartida en escuelas del sector público mediante sistema a distancia, educación para necesidades especiales impartida en escuelas del sector público mediante sistema abierto, educación para necesidades especiales impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación preescolar del sector público para necesidades especiales, servicios educativos, escuelas de educación primaria del sector público para necesidades especi	t	\N	\N
888	Escuelas de educación técnica superior del sector privado	educación técnica superior impartida en escuelas del sector privado mediante sistema a distancia, educación técnica superior impartida en escuelas del sector privado mediante sistema abierto, educación técnica superior impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de educación técnica superior del sector privado, servicios educativos, escuelas del sector privado para la formación de técnicos superiores en aviación, servicios educativos, escuelas del sector priv	t	\N	\N
889	Escuelas de educación técnica superior del sector público	educación técnica superior impartida en escuelas del sector público mediante sistema a distancia, educación técnica superior impartida en escuelas del sector público mediante sistema abierto, educación técnica superior impartida en escuelas del sector público mediante sistema escolarizado, escuelas de educación técnica superior del sector público, servicios educativos, escuelas del sector público para la formación de policías con grado de profesional técnico, servicios educativos, escuelas del s	t	\N	\N
890	Escuelas de educación superior del sector privado	colegios de educación superior del sector privado, servicios educativos, educación superior impartida en escuelas del sector privado mediante sistema a distancia, educación superior impartida en escuelas del sector privado mediante sistema abierto, educación superior impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de arte a nivel superior del sector privado, servicios educativos, escuelas de educación normal superior del sector privado, servicios educativos, escu	t	\N	\N
891	Escuelas de educación superior del sector público	colegios militares de educación superior, servicios educativos, educación superior impartida en escuelas del sector público mediante sistema a distancia, educación superior impartida en escuelas del sector público mediante sistema abierto, educación superior impartida en escuelas del sector público mediante sistema escolarizado, escuelas de arte a nivel superior del sector público, servicios educativos, escuelas de educación normal superior del sector público, servicios educativos, escuelas de e	t	\N	\N
892	Escuelas comerciales y secretariales del sector privado	capacitación técnica comercial y secretarial impartida en escuelas del sector privado mediante sistema a distancia, capacitación técnica comercial y secretarial impartida en escuelas del sector privado mediante sistema abierto, capacitación técnica comercial y secretarial impartida en escuelas del sector privado mediante sistema escolarizado, escuelas comerciales del sector privado, servicios educativos, escuelas del sector privado que proporcionan capacitación técnica comercial, servicios educa	t	\N	\N
893	Escuelas comerciales y secretariales del sector público	capacitación técnica comercial y secretarial impartida en escuelas del sector público mediante sistema a distancia, capacitación técnica comercial y secretarial impartida en escuelas del sector público mediante sistema abierto, capacitación técnica comercial y secretarial impartida en escuelas del sector público mediante sistema escolarizado, escuelas comerciales del sector público, servicios educativos, escuelas del sector público que proporcionan capacitación técnica comercial, servicios educa	t	\N	\N
894	Escuelas de computación del sector privado	capacitación técnica para el desarrollo de habilidades computacionales impartida en escuelas del sector privado mediante sistema a distancia, capacitación técnica para el desarrollo de habilidades computacionales impartida en escuelas del sector privado mediante sistema abierto, capacitación técnica para el desarrollo de habilidades computacionales impartida en escuelas del sector privado mediante sistema escolarizado, certificaciones de tecnologías de información (TI) otorgadas por el sector pr	t	\N	\N
895	Escuelas de computación del sector público	capacitación técnica para el desarrollo de habilidades computacionales impartida en escuelas del sector público mediante sistema a distancia, capacitación técnica para el desarrollo de habilidades computacionales impartida en escuelas del sector público mediante sistema abierto, capacitación técnica para el desarrollo de habilidades computacionales impartida en escuelas del sector público mediante sistema escolarizado, certificaciones de tecnologías de información (TI) otorgadas por el sector pú	t	\N	\N
896	Escuelas para la capacitación de ejecutivos del sector privado	capacitación de ejecutivos impartida en escuelas del sector privado mediante sistema a distancia, capacitación de ejecutivos impartida en escuelas del sector privado mediante sistema abierto, capacitación de ejecutivos impartida en escuelas del sector privado mediante sistema escolarizado, escuelas del sector privado que proporcionan capacitación a ejecutivos sobre aspectos de finanzas y alta dirección, servicios educativos, escuelas para la capacitación de ejecutivos del sector privado, servici	t	\N	\N
897	Escuelas para la capacitación de ejecutivos del sector público	capacitación de ejecutivos impartida en escuelas del sector público mediante sistema a distancia, capacitación de ejecutivos impartida en escuelas del sector público mediante sistema abierto, capacitación de ejecutivos impartida en escuelas del sector público mediante sistema escolarizado, escuelas del sector público que proporcionan capacitación a ejecutivos sobre aspectos de finanzas y alta dirección, servicios educativos, escuelas para la capacitación de ejecutivos del sector público, servici	t	\N	\N
898	Escuelas del sector privado dedicadas a la enseñanza de oficios	enseñanza de oficios impartida en escuelas del sector privado mediante sistema a distancia, enseñanza de oficios impartida en escuelas del sector privado mediante sistema abierto, enseñanza de oficios impartida en escuelas del sector privado mediante sistema escolarizado, escuelas del sector privado para la capacitación técnica como barman, servicios educativos, escuelas del sector privado para la capacitación técnica como electricista, servicios educativos, escuelas del sector privado para la c	t	\N	\N
899	Escuelas del sector público dedicadas a la enseñanza de oficios	enseñanza de oficios impartida en escuelas del sector público mediante sistema a distancia, enseñanza de oficios impartida en escuelas del sector público mediante sistema abierto, enseñanza de oficios impartida en escuelas del sector público mediante sistema escolarizado, escuelas del sector público para la capacitación técnica como barman, servicios educativos, escuelas del sector público para la capacitación técnica como electricista, servicios educativos, escuelas del sector público para la c	t	\N	\N
900	Escuelas de arte del sector privado	educación artística no formal impartida en escuelas del sector privado mediante sistema a distancia, educación artística no formal impartida en escuelas del sector privado mediante sistema abierto, educación artística no formal impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de artes plásticas del sector privado, servicios educativos, escuelas de danza del sector privado, servicios educativos, escuelas de escultura del sector privado, servicios educativos, escuel	t	\N	\N
901	Escuelas de arte del sector público	educación artística no formal impartida en escuelas del sector público mediante sistema a distancia, educación artística no formal impartida en escuelas del sector público mediante sistema abierto, educación artística no formal impartida en escuelas del sector público mediante sistema escolarizado, escuelas de artes plásticas del sector público, servicios educativos, escuelas de danza del sector público, servicios educativos, escuelas de escultura del sector público, servicios educativos, escuel	t	\N	\N
902	Escuelas de deporte del sector privado	entrenadores que trabajan por cuenta propia y sólo se dedican a la enseñanza de algún deporte, escuelas de aeróbics y zumba del sector privado, servicios educativos, escuelas de artes marciales del sector privado, servicios educativos, escuelas de equitación del sector privado, servicios educativos, escuelas de futbol del sector privado, servicios educativos, escuelas de gimnasia del sector privado, servicios educativos, escuelas de natación del sector privado, servicios educativos, escuelas de 	t	\N	\N
903	Escuelas de deporte del sector público	escuelas de aeróbics y zumba del sector público, servicios educativos, escuelas de artes marciales del sector público, servicios educativos, escuelas de equitación del sector público, servicios educativos, escuelas de futbol del sector público, servicios educativos, escuelas de gimnasia del sector público, servicios educativos, escuelas de natación del sector público, servicios educativos, escuelas de tenis del sector público, servicios educativos, escuelas de yoga del sector público, servicios 	t	\N	\N
904	Escuelas de idiomas del sector privado	cursos de preparación impartidos por escuelas de idiomas del sector privado para presentar exámenes de acreditación de segunda lengua, enseñanza no formal de idiomas impartida en escuelas del sector privado mediante sistema a distancia, enseñanza no formal de idiomas impartida en escuelas del sector privado mediante sistema abierto, enseñanza no formal de idiomas impartida en escuelas del sector privado mediante sistema escolarizado, escuelas de idiomas del sector privado, servicios educativos, 	t	\N	\N
905	Escuelas de idiomas del sector público	cursos de preparación impartidos por escuelas de idiomas del sector público para presentar exámenes de acreditación de segunda lengua, enseñanza no formal de idiomas impartida en escuelas del sector público mediante sistema a distancia, enseñanza no formal de idiomas impartida en escuelas del sector público mediante sistema abierto, enseñanza no formal de idiomas impartida en escuelas del sector público mediante sistema escolarizado, escuelas de idiomas del sector público, servicios educativos, 	t	\N	\N
906	Servicios de profesores particulares	clases de diferentes materias y niveles educativos impartidas por profesores particulares, preparación impartida por profesores particulares para presentar exámenes, regularización de estudiantes por profesores particulares, servicios de profesores particulares de manera presencial, servicios de profesores particulares en línea, tutoría académica para educación postsecundaria, tutoría académica para educación preescolar, primaria y secundaria	t	\N	\N
907	Otros servicios educativos proporcionados por el sector privado	clases de ecología impartidas por el sector privado, clases de educación vial impartidas por el sector privado, clases de robótica impartidas por el sector privado, cursos de actualización para maestros impartidos por el sector privado, cursos de motivación impartidos por el sector privado, cursos de oratoria y para hablar en público impartidos por el sector privado, cursos de personalidad impartidos por el sector privado, cursos de preparación impartidos por el sector privado para presentar exá	t	\N	\N
908	Otros servicios educativos proporcionados por el sector público	clases de ecología impartidas por el sector público, clases de educación vial impartidas por el sector público, clases de robótica impartidas por el sector público, cursos de actualización para maestros impartidos por el sector público, cursos de motivación impartidos por el sector público, cursos de oratoria y para hablar en público impartidos por el sector público, cursos de personalidad impartidos por el sector público, cursos de preparación impartidos por el sector público para presentar exá	t	\N	\N
909	Servicios de apoyo a la educación	centros de intercambio cultural, servicios de, centros de orientación vocacional, servicios de, desarrollo y administración de programas de apoyo para intercambio académico, didáctica, servicios de, diseño de exámenes, educación, consultoría, elaboración y diseño de materiales educativos, evaluación y diseño de currícula educativa, evaluación y diseño de programas educativos, gestión de becas, orientación vocacional, pedagogía, servicios de	t	\N	\N
910	Consultorios de medicina general del sector privado	consulta médica externa general, servicios del sector privado, consultorios de medicina general del sector privado, servicios de	t	\N	\N
911	Consultorios de medicina general del sector público	consulta médica externa general, servicios del sector público, consultorios de medicina general del sector público, servicios de	t	\N	\N
912	Consultorios de medicina especializada del sector privado	alergología, servicios médicos especializados del sector privado, anestesiología, servicios médicos especializados del sector privado, cardiología, servicios médicos especializados del sector privado, cirugía plástica, servicios médicos especializados del sector privado, cirugía, servicios médicos especializados del sector privado, consulta médica externa especializada, servicios del sector privado, control de peso con prescripción médica, servicios médicos especializados del sector privado, der	t	\N	\N
913	Consultorios de medicina especializada del sector público	alergología, servicios médicos especializados del sector público, anestesiología, servicios médicos especializados del sector público, cardiología, servicios médicos especializados del sector público, cirugía plástica, servicios médicos especializados del sector público, cirugía, servicios médicos especializados del sector público, consulta médica externa especializada, servicios del sector público, control de peso con prescripción médica, servicios médicos especializados del sector público, der	t	\N	\N
914	Clínicas de consultorios médicos del sector privado	clínicas de consultorios médicos del sector privado, consulta médica externa especializada en clínicas de consultorios del sector privado, consulta médica externa general en clínicas de consultorios del sector privado	t	\N	\N
915	Clínicas de consultorios médicos del sector público	clínicas de consultorios médicos del sector público, consulta médica externa especializada en clínicas de consultorios del sector público, consulta médica externa general en clínicas de consultorios del sector público	t	\N	\N
916	Consultorios dentales del sector privado	blanqueamiento dental en consultorios dentales del sector privado, cirugía dental en consultorios dentales del sector privado, cirugía maxilofacial en consultorios dentales del sector privado, consulta médica dental en consultorios dentales del sector privado, consultorios dentales del sector privado, servicios de, cosmetología dental en consultorios dentales del sector privado, endodoncia en consultorios dentales del sector privado, exodoncia en consultorios dentales del sector privado, implant	t	\N	\N
917	Consultorios dentales del sector público	blanqueamiento dental en consultorios dentales del sector público, cirugía dental en consultorios dentales del sector público, cirugía maxilofacial en consultorios dentales del sector público, consulta médica dental en consultorios dentales del sector público, consultorios dentales del sector público, servicios de, cosmetología dental en consultorios dentales del sector público, endodoncia en consultorios dentales del sector público, exodoncia en consultorios dentales del sector público, implant	t	\N	\N
918	Consultorios de quiropráctica del sector privado	consulta quiropráctica en consultorios del sector privado, terapia quiropráctica en consultorios del sector privado	t	\N	\N
919	Consultorios de quiropráctica del sector público	consulta quiropráctica en consultorios del sector público, terapia quiropráctica en consultorios del sector público	t	\N	\N
920	Consultorios de optometría	optometría, servicios de	t	\N	\N
925	Consultorios de nutriólogos y dietistas del sector privado	consulta en nutrición, servicios del sector privado, control de peso mediante dietas sin prescripción médica en consultorios del sector privado, dietética en consultorios del sector privado, servicios de, tratamientos alimenticios para el control y reducción de peso en consultorios del sector privado, tratamientos alimenticios para la atención de padecimientos en consultorios del sector privado	t	\N	\N
926	Consultorios de nutriólogos y dietistas del sector público	consulta en nutrición, servicios del sector público, control de peso mediante dietas sin prescripción médica en consultorios del sector público, dietética en consultorios del sector público, servicios de, tratamientos alimenticios para el control y reducción de peso en consultorios del sector público, tratamientos alimenticios para la atención de padecimientos en consultorios del sector público	t	\N	\N
927	Otros consultorios del sector privado para el cuidado de la salud	acupuntura en consultorios del sector privado, servicios de, consulta en naturismo, servicios del sector privado, hipnoterapia en consultorios del sector privado, servicios de, masajes terapéuticos en consultorios del sector privado, servicios de, parteras del sector privado, servicios de, podiatría en consultorios del sector privado, servicios de, podología en consultorios del sector privado, servicios de	t	\N	\N
928	Otros consultorios del sector público para el cuidado de la salud	acupuntura en consultorios del sector público, servicios de, consulta en naturismo, servicios del sector público, hipnoterapia en consultorios del sector público, servicios de, masajes terapéuticos en consultorios del sector público, servicios de, parteras del sector público, servicios de, podiatría en consultorios del sector público, servicios de, podología en consultorios del sector público, servicios de	t	\N	\N
929	Centros de planificación familiar del sector privado	atención médica para el control de la natalidad del sector privado, atención médica prenatal del sector privado, atención psicoprofiláctica del sector privado, centros de planificación familiar del sector privado, servicios de, consulta de planificación familiar en centros de planificación familiar del sector privado, consulta de problemas de fertilidad en centros de planificación familiar del sector privado, salpingoclasia en centros de planificación familiar del sector privado, servicios de, t	t	\N	\N
930	Centros de planificación familiar del sector público	atención médica para el control de la natalidad del sector público, atención médica prenatal proporcionada por el sector público, atención psicoprofiláctica proporcionada por el sector público, centros de planificación familiar del sector público, servicios de, consulta de planificación familiar en centros de planificación familiar del sector público, consulta de problemas de fertilidad en centros de planificación familiar del sector público, salpingoclasia en centros de planificación familiar d	t	\N	\N
931	Centros del sector privado de atención médica externa para enfermos mentales y adictos	atención médica externa para la rehabilitación de adictos en centros del sector privado, atención médica externa para la rehabilitación de enfermos mentales en centros del sector privado, atención médica externa para problemas de alcoholismo en centros del sector privado, atención médica externa para problemas de drogadicción en centros del sector privado, desintoxicación en centros de atención médica externa del sector privado, terapia física para la rehabilitación de enfermos mentales y adicto	t	\N	\N
932	Centros del sector público de atención médica externa para enfermos mentales y adictos	atención médica externa para la rehabilitación de adictos en centros del sector público, atención médica externa para la rehabilitación de enfermos mentales en centros del sector público, atención médica externa para problemas de alcoholismo en centros del sector público, atención médica externa para problemas de drogadicción en centros del sector público, desintoxicación en centros de atención médica externa del sector público, terapia física para la rehabilitación de enfermos mentales y adicto	t	\N	\N
933	Otros centros del sector privado para la atención de pacientes que no requieren hospitalización	clínicas de cirugía ambulatoria del sector privado, servicios de, clínicas de diálisis del sector privado, servicios de, tratamiento de diálisis peritoneal en centros del sector privado, tratamiento de diálisis renal en centros del sector privado, tratamiento de hemodiálisis en centros del sector privado	t	\N	\N
934	Otros centros del sector público para la atención de pacientes que no requieren hospitalización	clínicas de cirugía ambulatoria del sector público, servicios de, clínicas de diálisis del sector público, servicios de, tratamiento de diálisis peritoneal en centros del sector público, tratamiento de diálisis renal en centros del sector público, tratamiento de hemodiálisis en centros del sector público	t	\N	\N
935	Laboratorios médicos y de diagnóstico del sector privado	análisis bioquímicos para personas en laboratorios del sector privado, análisis clínicos en laboratorios del sector privado, análisis clínicos para personas en laboratorios del sector privado, análisis hematológicos para personas en laboratorios del sector privado, análisis histopatológicos para personas en laboratorios del sector privado, análisis hormonales para personas en laboratorios del sector privado, análisis inmunológicos para personas en laboratorios del sector privado, análisis medico	t	\N	\N
936	Laboratorios médicos y de diagnóstico del sector público	análisis bioquímicos para personas en laboratorios del sector público, análisis clínicos en laboratorios del sector público, análisis clínicos para personas en laboratorios del sector público, análisis hematológicos para personas en laboratorios del sector público, análisis histopatológicos para personas en laboratorios del sector público, análisis hormonales para personas en laboratorios del sector público, análisis inmunológicos para personas en laboratorios del sector público, análisis medico	t	\N	\N
937	Servicios de enfermería a domicilio	enfermeras que trabajan por su cuenta, enfermería a domicilio por cuidadoras, enfermería a domicilio por enfermeras especializadas, enfermería a domicilio por enfermeras generales, terapia mediante infusiones a domicilio	t	\N	\N
938	Servicios de ambulancias	buceo de rescate, búsqueda y rescate de personas, servicios de, escolta médica de pacientes, órganos, tejidos, células y especímenes, traslado de, permanencia de servicios médicos de urgencia con o sin traslados de ambulancia en eventos, primeros auxilios en establecimientos, servicios de, traslado de enfermos en ambulancias, traslado y atención médica de no urgencia con cuidados de soporte avanzado de vida en ambulancias de superficie, traslado y atención médica de no urgencia con cuidados de s	t	\N	\N
955	Orfanatos y otras residencias de asistencia social del sector privado	casas cuna del sector privado, servicios de, casas para jóvenes con padres delincuentes, servicios prestados por el sector privado, hogares del sector privado para madres divorciadas, servicios de, hogares del sector privado para madres solteras, servicios de, hogares del sector privado para personas con discapacidad, servicios de, orfanatos del sector privado, servicios de	t	\N	\N
939	Servicios de bancos de órganos, bancos de sangre y otros servicios auxiliares al tratamiento médico prestados por el sector privado	aplicación de vacunas por el sector privado, bancos de células germinales o células madre del sector privado, bancos de esperma humano del sector privado, bancos de ojos del sector privado, bancos de órganos del sector privado, bancos de sangre del sector privado para las personas, bancos de semen humano del sector privado, bancos de tejidos del sector privado, centros de donación de órganos del sector privado, servicios de, centros de donación de sangre del sector privado, servicios de, centros	t	\N	\N
940	Servicios de bancos de órganos, bancos de sangre y otros servicios auxiliares al tratamiento médico prestados por el sector público	aplicación de vacunas por el sector público, bancos de células germinales o células madre del sector público, bancos de esperma humano del sector público, bancos de ojos del sector público, bancos de órganos del sector público, bancos de sangre del sector público para las personas, bancos de semen humano del sector público, bancos de tejidos del sector público, centros de donación de órganos del sector público, servicios de, centros de donación de sangre del sector público, servicios de, centros	t	\N	\N
941	Hospitales generales del sector privado	hospitales de enfermedades de la mujer del sector privado, servicios médicos en, hospitales generales del sector privado, servicios médicos, hospitales geriátricos del sector privado, servicios médicos, hospitales pediátricos del sector privado, servicios médicos	t	\N	\N
942	Hospitales generales del sector público	hospitales de enfermedades de la mujer del sector público, servicios médicos, hospitales generales del sector público, servicios médicos, hospitales geriátricos del sector público, servicios médicos, hospitales pediátricos del sector público, servicios médicos	t	\N	\N
943	Hospitales psiquiátricos y para el tratamiento por adicción del sector privado	hospitales para el tratamiento de alcoholismo del sector privado, servicios médicos, hospitales para el tratamiento de esquizofrenia del sector privado, servicios médicos, hospitales para el tratamiento de hipocondría del sector privado, servicios médicos, hospitales para el tratamiento de neurosis del sector privado, servicios médicos, hospitales para el tratamiento de paranoia del sector privado, servicios médicos, hospitales para el tratamiento de trastornos psicológicos del sector privado, s	t	\N	\N
944	Hospitales psiquiátricos y para el tratamiento por adicción del sector público	hospitales para el tratamiento de alcoholismo del sector público, servicios médicos, hospitales para el tratamiento de esquizofrenia del sector público, servicios médicos, hospitales para el tratamiento de hipocondría del sector público, servicios médicos en, hospitales para el tratamiento de neurosis del sector público, servicios médicos en, hospitales para el tratamiento de paranoia del sector público, servicios médicos en, hospitales para el tratamiento de trastornos psicológicos del sector p	t	\N	\N
945	Hospitales del sector privado de otras especialidades médicas	hospitales de maternidad del sector privado, servicios médicos, hospitales del sector privado especializados en cardiología, servicios médicos, hospitales del sector privado especializados en cirugía estética, servicios médicos, hospitales del sector privado especializados en gineco-obstetricia, servicios médicos, hospitales del sector privado especializados en neumología, servicios médicos, hospitales del sector privado especializados en neurocirugía, servicios médicos, hospitales del sector pr	t	\N	\N
946	Hospitales del sector público de otras especialidades médicas	hospitales de maternidad del sector público, servicios médicos, hospitales del sector público especializados en cardiología, servicios médicos, hospitales del sector público especializados en cirugía estética, servicios médicos, hospitales del sector público especializados en gineco-obstetricia, servicios médicos, hospitales del sector público especializados en neumología, servicios médicos, hospitales del sector público especializados en neurocirugía, servicios médicos, hospitales del sector pú	t	\N	\N
947	Residencias del sector privado con cuidados de enfermeras para enfermos convalecientes, en rehabilitación, incurables y terminales	casas de reposo físico del sector privado con cuidados de enfermeras, centros de convalecencia del sector privado con cuidados de enfermeras, residencias del sector privado con cuidados de enfermeras para enfermos convalecientes, residencias del sector privado con cuidados de enfermeras para enfermos en rehabilitación, residencias del sector privado con cuidados de enfermeras para enfermos incurables, residencias del sector privado con cuidados de enfermeras para enfermos terminales, residencias	t	\N	\N
948	Residencias del sector público con cuidados de enfermeras para enfermos convalecientes, en rehabilitación, incurables y terminales	casas de reposo físico del sector público con cuidados de enfermeras, centros de convalecencia del sector público con cuidados de enfermeras, residencias del sector público con cuidados de enfermeras para enfermos convalecientes, residencias del sector público con cuidados de enfermeras para enfermos en rehabilitación, residencias del sector público con cuidados de enfermeras para enfermos incurables, residencias del sector público con cuidados de enfermeras para enfermos terminales, residencias	t	\N	\N
949	Residencias del sector privado para el cuidado de personas con problemas de retardo mental	residencias del sector privado con asistencia para realizar actividades de la vida cotidiana y servicios de rehabilitación mental, residencias del sector privado para el cuidado de personas con retardo mental, servicios de	t	\N	\N
950	Residencias del sector público para el cuidado de personas con problemas de retardo mental	residencias del sector público con asistencia para realizar actividades de la vida cotidiana y servicios de rehabilitación mental, residencias del sector público para el cuidado de personas con retardo mental, servicios de	t	\N	\N
951	Residencias del sector privado para el cuidado de personas con problemas de trastorno mental y adicción	residencias del sector privado con servicios de alojamiento, alimentación, evaluación médica, desintoxicación y terapia por adicción, residencias del sector privado para el cuidado de personas con problemas de adicción, servicios de, residencias del sector privado para el cuidado de personas con problemas de trastorno mental, servicios de, residencias del sector privado para el cuidado de personas que padecen adicción a sustancias químicas, servicios de, residencias del sector privado para el cu	t	\N	\N
952	Residencias del sector público para el cuidado de personas con problemas de trastorno mental y adicción	residencias del sector público con servicios de alojamiento, alimentación, evaluación médica, desintoxicación y terapia por adicción, residencias del sector público para el cuidado de personas con problemas de adicción, servicios de, residencias del sector público para el cuidado de personas con problemas de trastorno mental, servicios de, residencias del sector público para el cuidado de personas que padecen adicción a sustancias químicas, servicios de, residencias del sector público para el cu	t	\N	\N
956	Orfanatos y otras residencias de asistencia social del sector público	albergues escolares del sector público, servicios de, casas cuna del sector público, servicios de, casas de estudiantes (residencias de asistencia social), servicios de, casas para jóvenes con padres delincuentes, servicios prestados por el sector público, hogares del sector público para madres divorciadas, servicios de, hogares del sector público para madres solteras, servicios de, hogares del sector público para personas con discapacidad, servicios de, orfanatos del sector público, servicios d	t	\N	\N
957	Servicios de orientación y trabajo social para la niñez y la juventud prestados por el sector privado	adopción del sector privado, servicios de, ayuda vía telefónica para niños y jóvenes en situación de crisis, servicios del sector privado, centros de integración juvenil del sector privado, servicios de, entrenamiento de habilidades y desarrollo social positivo para niños y jóvenes, servicios del sector privado, integración social para niños y jóvenes, servicios del sector privado, orientación para niños, jóvenes y familias para prevenir adicciones, servicios del sector privado, orientación sexu	t	\N	\N
958	Servicios de orientación y trabajo social para la niñez y la juventud prestados por el sector público	adopción del sector público, servicios de, ayuda vía telefónica para niños y jóvenes en situación de crisis, servicios del sector público, centros de integración juvenil del sector público, servicios de, entrenamiento de habilidades y desarrollo social positivo para niños y jóvenes, servicios del sector público, integración social para niños y jóvenes, servicios del sector público, orientación para niños, jóvenes y familias para prevenir adicciones, servicios del sector público, orientación sexu	t	\N	\N
959	Centros del sector privado dedicados a la atención y cuidado diurno de ancianos y personas con discapacidad	atención y cuidado diurno de ancianos en guarderías del sector privado, atención y cuidado diurno de ancianos y personas con discapacidad en centros del sector privado, atención y cuidado diurno de personas con discapacidad en guarderías del sector privado, integración social para adultos con discapacidad, servicios del sector privado, integración social para ancianos, servicios del sector privado, rehabilitación profesional para adultos con discapacidad, servicios del sector privado	t	\N	\N
960	Centros del sector público dedicados a la atención y cuidado diurno de ancianos y personas con discapacidad	atención y cuidado diurno de ancianos en guarderías del sector público, atención y cuidado diurno de ancianos y personas con discapacidad en centros del sector público, atención y cuidado diurno de personas con discapacidad en guarderías del sector público, integración social para adultos con discapacidad, servicios del sector público, integración social para ancianos, servicios del sector público, rehabilitación profesional para adultos con discapacidad, servicios del sector público	t	\N	\N
961	Agrupaciones de autoayuda para alcohólicos y personas con otras adicciones	agrupaciones de alcohólicos anónimos, agrupaciones de apoyo a familiares de personas con alguna adición, agrupaciones de apoyo a familiares de personas con alguna enfermedad terminal, agrupaciones de autoayuda para alcohólicos, agrupaciones de autoayuda para comedores compulsivos, agrupaciones de autoayuda para drogadictos, agrupaciones de autoayuda para familiares de adictos, agrupaciones de autoayuda para neuróticos, agrupaciones de autoayuda para padres de hijos con parálisis cerebral, agrupa	t	\N	\N
962	Otros servicios de orientación y trabajo social prestados por el sector privado	asistencia social para inmigrantes y refugiados, servicios del sector privado, centros del sector privado para la asistencia psicológica y legal de mujeres violadas, servicios de, centros del sector privado para la orientación de mujeres violadas, servicios de, centros del sector privado para la orientación matrimonial, servicios de, orientación a personas con problemas de drogadicción prestados por el sector privado, orientación sobre planificación familiar sin atención médica prestados por el 	t	\N	\N
963	Otros servicios de orientación y trabajo social prestados por el sector público	asistencia social para inmigrantes y refugiados, servicios del sector público, centros del sector público para la asistencia psicológica y legal de mujeres violadas, servicios de, centros del sector público para la orientación de mujeres violadas, servicios de, centros del sector público para la orientación matrimonial, servicios de, orientación a personas con problemas de drogadicción prestados por el sector público, orientación sobre planificación familiar sin atención médica prestados por el 	t	\N	\N
964	Servicios de alimentación comunitarios prestados por el sector privado	acopio, almacenamiento y distribución de alimentos y otros artículos domésticos para comedores de beneficencia e instituciones de ayuda, servicios del sector privado, alimentación a personas afectadas por catástrofes, servicios prestados por el sector privado, alimentación a personas afectadas por indigencia, servicios prestados por el sector privado, alimentación a personas afectadas por siniestros, servicios prestados por el sector privado, comedores del sector privado para indigentes, servici	t	\N	\N
965	Servicios de alimentación comunitarios prestados por el sector público	acopio, almacenamiento y distribución de alimentos y otros artículos domésticos para comedores de beneficencia e instituciones de ayuda, servicios del sector público, alimentación a personas afectadas por catástrofes, servicios prestados por el sector público, alimentación a personas afectadas por indigencia, servicios prestados por el sector público, alimentación a personas afectadas por siniestros, servicios prestados por el sector público, comedores del sector público para indigentes, servici	t	\N	\N
966	Refugios temporales comunitarios del sector privado	albergues del sector privado para migrantes, servicios de, refugios temporales comunitarios del sector privado, servicios de, refugios temporales del sector privado para familias de niños enfermos, servicios de, refugios temporales del sector privado para indigentes, servicios de, refugios temporales del sector privado para migrantes, servicios de, refugios temporales del sector privado para mujeres víctimas de asalto sexual, servicios de, refugios temporales del sector privado para mujeres víct	t	\N	\N
967	Refugios temporales comunitarios del sector público	albergues del sector público para migrantes, servicios de, refugios temporales comunitarios del sector público, servicios de, refugios temporales del sector público para familias de niños enfermos, servicios de, refugios temporales del sector público para indigentes, servicios de, refugios temporales del sector público para migrantes, servicios de, refugios temporales del sector público para mujeres víctimas de asalto sexual, servicios de, refugios temporales del sector público para mujeres víct	t	\N	\N
968	Servicios de emergencia comunitarios prestados por el sector privado	refugios alpinos del sector privado, servicios de, refugios temporales del sector privado para personas afectadas por catástrofes, servicios de, refugios temporales del sector privado para personas afectadas por siniestros, servicios de	t	\N	\N
970	Servicios de capacitación para el trabajo prestados por el sector privado para personas desempleadas, subempleadas o con discapacidad	capacitación para el trabajo para personas con discapacidad, servicios prestados por el sector privado, capacitación para el trabajo para personas desempleadas, servicios prestados por el sector privado, capacitación para el trabajo para personas que por las condiciones del mercado laboral no tienen una perspectiva de empleo a corto plazo, servicios prestados por el sector privado, capacitación para el trabajo para personas subempleadas, servicios prestados por el sector privado	t	\N	\N
971	Servicios de capacitación para el trabajo prestados por el sector público para personas desempleadas, subempleadas o con discapacidad	capacitación para el trabajo para personas con discapacidad, servicios prestados por el sector público, capacitación para el trabajo para personas desempleadas, servicios prestados por el sector público, capacitación para el trabajo para personas que por las condiciones del mercado laboral no tienen una perspectiva de empleo a corto plazo, servicios prestados por el sector público, capacitación para el trabajo para personas subempleadas, servicios prestados por el sector público	t	\N	\N
972	Guarderías del sector privado	centros de estimulación temprana del sector privado, servicios de, cuidado diario de niños, servicios prestados por el sector privado, guarderías del sector privado, servicios de	t	\N	\N
973	Guarderías del sector público	centros de estimulación temprana del sector público, servicios de, cuidado diario de niños, servicios prestados por el sector público, guarderías del sector público, servicios de	t	\N	\N
974	Compañías de teatro del sector privado	admisión a espectáculos de teatro u ópera en vivo ofrecidos por el sector privado, compañías de burlesque del sector privado, compañías de comediantes del sector privado, compañías de marionetas del sector privado, compañías de mimos del sector privado, compañías de ópera del sector privado, compañías de teatro de revista del sector privado, compañías de teatro del sector privado, compañías de teatro del sector privado que combinan su actividad con el alquiler de sus instalaciones, compañías de 	t	\N	\N
975	Compañías de teatro del sector público	admisión a espectáculos de teatro u ópera en vivo ofrecidos por el sector público, compañías de burlesque del sector público, compañías de comediantes del sector público, compañías de marionetas del sector público, compañías de mimos del sector público, compañías de ópera del sector público, compañías de teatro de revista del sector público, compañías de teatro del sector público, compañías de teatro del sector público que combinan su actividad con el alquiler de sus instalaciones, compañías de 	t	\N	\N
976	Compañías de danza del sector privado	admisión a espectáculos de danza en vivo ofrecidos por el sector privado, compañías de ballet del sector privado, compañías de capoeira del sector privado, compañías de danza clásica del sector privado, compañías de danza contemporánea del sector privado, compañías de danza del sector privado, compañías de danza del sector privado que combinan su actividad con el alquiler de sus instalaciones, compañías de danza folklórica del sector privado, compañías de danza moderna del sector privado, compañ	t	\N	\N
977	Compañías de danza del sector público	admisión a espectáculos de danza en vivo ofrecidos por el sector público, compañías de ballet del sector público, compañías de capoeira del sector público, compañías de danza clásica del sector público, compañías de danza contemporánea del sector público, compañías de danza del sector público, compañías de danza del sector público que combinan su actividad con el alquiler de sus instalaciones, compañías de danza folklórica del sector público, compañías de danza moderna del sector público, compañ	t	\N	\N
978	Cantantes y grupos musicales del sector privado	admisión a espectáculos musicales ofrecidos por el sector privado, bandas musicales del sector privado, cantantes que trabajan por cuenta propia, cantantes y grupos musicales del sector privado que combinan su actividad con el alquiler de sus instalaciones, servicios de, concertistas del sector privado, servicios de, conjuntos musicales del sector privado, coros del sector privado, espectáculos musicales ofrecidos por el sector privado, producción y presentación, grupos musicales del sector priv	t	\N	\N
979	Grupos musicales del sector público	admisión a espectáculos musicales ofrecidos por el sector público, bandas municipales, bandas musicales del sector público, coros del sector público, espectáculos musicales ofrecidos por el sector público, producción y presentación, grupos musicales del sector público, grupos musicales del sector público que combinan su actividad con el alquiler de sus instalaciones, orquestas del sector público, producción y presentación de espectáculos musicales del sector público en combinación con la promoci	t	\N	\N
980	Otras compañías y grupos de espectáculos artísticos del sector privado	admisión a espectáculos circenses, de magia y patinaje en vivo ofrecidos por el sector privado, compañías circenses del sector privado, compañías circenses del sector privado que combinan su actividad con el alquiler de sus instalaciones, compañías de carnavales del sector privado, compañías y grupos de magia del sector privado, compañías y grupos de magia del sector privado que combinan su actividad con el alquiler de sus instalaciones, compañías y grupos de patinaje del sector privado, compañí	t	\N	\N
981	Otras compañías y grupos de espectáculos artísticos del sector público	admisión a espectáculos de magia y patinaje en vivo ofrecidos por el sector público, compañías y grupos de magia del sector público, compañías y grupos de magia del sector público que combinan su actividad con el alquiler de sus instalaciones, compañías y grupos de patinaje del sector público, compañías y grupos de patinaje del sector público que combinan su actividad con el alquiler de sus instalaciones, espectáculos de magia del sector público, producción y presentación, espectáculos de patina	t	\N	\N
982	Deportistas profesionales	arbitraje de eventos deportivos, árbitros profesionales que trabajan por cuenta propia, atletas profesionales que trabajan por cuenta propia, boxeadores profesionales que trabajan por cuenta propia, corredores de autos profesionales que trabajan por cuenta propia, deportistas profesionales que combinan su actividad con el entrenamiento o la enseñanza deportiva, servicios de, deportistas profesionales que trabajan por cuenta propia, espectáculos deportivos por deportistas profesionales, presentac	t	\N	\N
983	Equipos deportivos profesionales	administradores de cuadrillas para la lidia de toros, servicios de, administradores de equipos para peleas de gallos, servicios de, administradores de equipos profesionales de carreras de automóviles, servicios de, administradores de equipos profesionales de carreras de caballos, servicios de, administradores de equipos profesionales de carreras de perros, servicios de, admisión a espectáculos deportivos en vivo, autódromos, servicios de, entrenamiento de animales de carreras y para otros espect	t	\N	\N
984	Promotores del sector privado de espectáculos artísticos, culturales, deportivos y similares que cuentan con instalaciones para presentarlos	manejo de eventos artísticos, culturales y deportivos por promotores del sector privado que cuentan con instalaciones, promotores del sector privado que combinan su actividad con el alquiler de sus instalaciones, promotores del sector privado que cuentan con instalaciones para la presentación de espectáculos artísticos, promotores del sector privado que cuentan con instalaciones para la presentación de espectáculos culturales, promotores del sector privado que cuentan con instalaciones para la p	t	\N	\N
985	Promotores del sector público de espectáculos artísticos, culturales, deportivos y similares que cuentan con instalaciones para presentarlos	casas de la cultura del sector público, manejo de eventos artísticos, culturales y deportivos por promotores del sector público que cuentan con instalaciones, promotores del sector público que combinan su actividad con el alquiler de sus instalaciones, promotores del sector público que cuentan con instalaciones para la presentación de espectáculos artísticos, promotores del sector público que cuentan con instalaciones para la presentación de espectáculos culturales, promotores del sector público	t	\N	\N
986	Promotores de espectáculos artísticos, culturales, deportivos y similares que no cuentan con instalaciones para presentarlos	manejo de eventos artísticos, culturales y deportivos por promotores que no cuentan con instalaciones, promotores que no cuentan con instalaciones para la presentación de espectáculos artísticos, promotores que no cuentan con instalaciones para la presentación de espectáculos culturales, promotores que no cuentan con instalaciones para la presentación de espectáculos deportivos, promotores que no cuentan con instalaciones para la presentación de ferias agrícolas, promotores que no cuentan con in	t	\N	\N
987	Agentes y representantes de artistas, deportistas y similares	actores y actrices, manejo de carrera de, actores y actrices, representación y administración de, agentes y representantes de artistas y deportistas, servicios de, artistas, representación y administración de, cantantes, manejo de carrera de, cantantes, representación y administración de, celebridades, representación y administración de, creativos, representación y administración de, deportistas, manejo de carrera de, deportistas, representación y administración de, entrenadores, representación 	t	\N	\N
988	Artistas, escritores y técnicos independientes	acróbatas que trabajan por cuenta propia, actores que trabajan por cuenta propia, actrices que trabajan por cuenta propia, artistas que trabajan por cuenta propia, atletas dedicados exclusivamente a ofrecer discursos o a hacer apariciones públicas por las cuales reciben honorarios, servicios de, backstage para espectáculos en vivo, bailarines que trabajan por cuenta propia, camarógrafos que trabajan por cuenta propia, caricaturistas que trabajan por cuenta propia, celebridades dedicadas exclusiv	t	\N	\N
989	Museos del sector privado	exposiciones itinerantes en museos del sector privado, alquiler, galerías de arte del sector privado, exhibición de colecciones en, herbarios del sector privado, exhibición de colecciones en, insectarios del sector privado, exhibición de colecciones en, museos de antropología del sector privado, exhibición de colecciones en, museos de arte contemporáneo del sector privado, exhibición de colecciones en, museos de arte del sector privado, exhibición de colecciones en, museos de artesanías del sect	t	\N	\N
990	Museos del sector público	exposiciones itinerantes en museos del sector público, alquiler, galerías de arte del sector público, exhibición de colecciones en, herbarios del sector público, exhibición de colecciones en, insectarios del sector público, exhibición de colecciones en, museos de antropología del sector público, exhibición de colecciones en, museos de arte contemporáneo del sector público, exhibición de colecciones en, museos de arte del sector público, exhibición de colecciones, museos de artesanías del sector 	t	\N	\N
991	Sitios históricos	acceso a edificios históricos, acceso a fuertes históricos, acceso a sitios históricos que cuentan con museo, acceso a zonas arqueológicas, visitas guiadas a sitios históricos	t	\N	\N
992	Jardines botánicos y zoológicos del sector privado	acuarios del sector privado, exhibición de animales en, aviarios del sector privado, exhibición de animales en, delfinarios del sector privado, exhibición de animales, jardines botánicos del sector privado, exhibición de plantas en, parques tipo safari del sector privado, exhibición de animales en, visitas guiadas a jardines botánicos y zoológicos del sector privado, zoológicos del sector privado, exhibición de animales en	t	\N	\N
993	Jardines botánicos y zoológicos del sector público	acuarios del sector público, exhibición de animales en, aviarios del sector público, exhibición de animales en, delfinarios del sector público, exhibición de animales, jardines botánicos del sector público, exhibición de plantas en, parques tipo safari del sector público, exhibición de animales en, visitas guiadas a jardines botánicos y zoológicos del sector público, zoológicos del sector público, exhibición de animales en	t	\N	\N
994	Grutas, parques naturales y otros sitios del patrimonio cultural de la nación	acceso a cascadas, acceso a cavernas, acceso a cenotes, acceso a grutas, acceso a parques de conservación, acceso a parques nacionales, acceso a parques naturales, acceso a reservas naturales, acceso a santuarios de animales, acceso a sitios del patrimonio cultural de la nación, acceso a zonas de monumentos artísticos, acceso a zonas naturales, acceso a zonas tradicionales, visitas guiadas a grutas, parques naturales y otros sitios del patrimonio cultural de la nación	t	\N	\N
995	Parques de diversiones y temáticos del sector privado	acceso a albercas de pelotas en parques de diversiones y temáticos del sector privado, acceso a juegos inflables en parques de diversiones y temáticos del sector privado, acceso a juegos y atracciones mecánicos en parques de diversiones y temáticos del sector privado, acceso a parques de diversiones del sector privado, acceso a parques temáticos del sector privado	t	\N	\N
996	Parques de diversiones y temáticos del sector público	acceso a albercas de pelotas en parques de diversiones y temáticos del sector público, acceso a juegos inflables en parques de diversiones y temáticos del sector público, acceso a juegos y atracciones mecánicos en parques temáticos del sector público, acceso a parques de diversiones del sector público, acceso a parques temáticos del sector público	t	\N	\N
997	Parques acuáticos y balnearios del sector privado	acceso a aguas termales en balnearios del sector privado, acceso a albercas del sector privado, acceso a balnearios del sector privado, acceso a instalaciones acuáticas del sector privado, acceso a parques acuáticos del sector privado, acceso a toboganes del sector privado, juegos y atracciones acuáticos en parques acuáticos y balnearios del sector privado	t	\N	\N
998	Parques acuáticos y balnearios del sector público	acceso a aguas termales en balnearios del sector público, acceso a albercas del sector público, acceso a balnearios del sector público, acceso a instalaciones acuáticas del sector público, acceso a parques acuáticos del sector público, acceso a toboganes del sector público, juegos y atracciones acuáticos en parques acuáticos y balnearios del sector público	t	\N	\N
999	Casas de juegos electrónicos	acceso a albercas de pelotas en casas de juegos electrónicos, acceso a casas de juegos electrónicos, entretenimiento en máquinas de juegos electrónicos que funcionan con monedas o fichas, entretenimiento en máquinas de juegos electrónicos que se cobran de acuerdo con el tiempo de uso, entretenimiento en máquinas de video juegos, juegos de video por computadora, servicios de	t	\N	\N
1000	Casinos	casinos, servicios de, entretenimiento mediante juegos de mesa y cartas con apuesta	t	\N	\N
1001	Venta de billetes de lotería, pronósticos deportivos y otros boletos de sorteo	administración de la Lotería Nacional para la Asistencia Pública, administración de Pronósticos Deportivos para la Asistencia Pública, billetes de lotería tradicional, venta de, boletos de rifas, venta de, boletos de sorteo, venta de, juegos de números, venta de, lotería instantánea, venta de, melate, venta de, progol, venta de, pronósticos deportivos, venta de	t	\N	\N
1002	Otros juegos de azar	entretenimiento en máquinas de apuestas que funcionan con monedas, juegos de azar en línea, recepción de apuestas contra el establecimiento en carreras, eventos deportivos y otros, recepción de apuestas contra otros jugadores en carreras, eventos deportivos y otros (sistema paramutual) efectuadas en el sitio del evento, recepción de apuestas contra otros jugadores en carreras, eventos deportivos y otros (sistema paramutual) efectuadas fuera del sitio del evento, recepción de apuestas en centros 	t	\N	\N
1003	Campos de golf	acceso a campos de golf en combinación con instalaciones para practicar otras actividades deportivas, acceso a clubes de golf, caddies, servicios de, instalaciones equipadas para jugar golf, servicios de	t	\N	\N
1004	Pistas para esquiar	operación de áreas para esquiar, operación de equipo en pistas para esquiar, pistas para esquiar, servicios de	t	\N	\N
1005	Marinas turísticas	almacenamiento de embarcaciones recreativas en marinas turísticas, almacenamiento de embarcaciones recreativas en tierra (marina seca), amarre de cabos para embarcaciones recreativas, amarre temporal para embarcaciones recreativas, anclaje de embarcaciones recreativas en agua (marina húmeda), atraques y desatraques para embarcaciones recreativas, clubes de yates que combinan su actividad con la operación de marinas turísticas, marinas turísticas, servicios de, operación de muelles para embarcaci	t	\N	\N
1006	Clubes deportivos del sector privado	acceso a clubes deportivos del sector privado	t	\N	\N
1007	Clubes deportivos del sector público	acceso a clubes deportivos del sector público	t	\N	\N
1008	Centros de acondicionamiento físico del sector privado	acceso a albercas olímpicas del sector privado, acceso a canchas de básquetbol del sector privado, acceso a canchas de béisbol del sector privado, acceso a canchas de frontenis del sector privado, acceso a canchas de frontón del sector privado, acceso a canchas de futbol del sector privado, acceso a canchas de futbol rápido del sector privado, acceso a canchas de squash del sector privado, acceso a canchas de tenis del sector privado, acceso a canchas de voleibol del sector privado, acceso a gim	t	\N	\N
1009	Centros de acondicionamiento físico del sector público	acceso a albercas olímpicas del sector público, acceso a canchas de básquetbol del sector público, acceso a canchas de béisbol del sector público, acceso a canchas de frontenis del sector público, acceso a canchas de frontón del sector público, acceso a canchas de futbol del sector público, acceso a canchas de futbol rápido del sector público, acceso a canchas de squash del sector público, acceso a canchas de tenis del sector público, acceso a canchas de voleibol del sector público, acceso a gim	t	\N	\N
1010	Boliches	admisión a instalaciones para jugar boliche, boliches con billar, servicios de, instalaciones equipadas para jugar boliche, servicios de	t	\N	\N
1011	Billares	instalaciones recreativas para jugar billar, servicios de, tiempo en mesas de carambola, tiempo en mesas de pool	t	\N	\N
1012	Clubes o ligas de aficionados	clubes de pasatiempos que cuentan con instalaciones, clubes de yates sin marinas turísticas, clubes o ligas de aficionados, clubes o ligas de aficionados de actividades deportivas, clubes o ligas de aficionados de actividades recreativas, clubes o ligas de aficionados de ajedrez, clubes o ligas de aficionados de aviación, clubes o ligas de aficionados de béisbol, clubes o ligas de aficionados de boliche, clubes o ligas de aficionados de bridge, clubes o ligas de aficionados de canotaje, clubes o	t	\N	\N
1013	Otros servicios recreativos prestados por el sector privado	acceso a campos de golf miniatura del sector privado, acceso a casas de terror del sector privado, acceso a pistas para carritos (go-karts) del sector privado, acceso a salas de tiro al blanco del sector privado, acceso a salones de baile del sector privado que no expenden bebidas alcohólicas, acceso a salones de ping-pong del sector privado, administración por el sector privado de máquinas de juegos electrónicos colocadas en otras unidades económicas, buceo recreativo prestados por el sector pr	t	\N	\N
1014	Otros servicios recreativos prestados por el sector público	acceso a salas de tiro al blanco del sector público, acceso a salones de ping-pong del sector público, ferias de juegos mecánicos del sector público, servicios recreativos en, juegos recreativos con premio en ferias del sector público, servicios de	t	\N	\N
1015	Hoteles con otros servicios integrados	alojamiento temporal mediante la modalidad de tiempos compartidos en hoteles con otros servicios integrados, hoteles que en la misma ubicación física ofrecen uno o más servicios integrados bajo la misma razón social, alojamiento temporal en, parques acuáticos y balnearios que en la misma ubicación física y bajo la misma razón social proporcionan alojamiento temporal	t	\N	\N
1016	Hoteles sin otros servicios integrados	hoteles sin otros servicios integrados, alojamiento temporal en	t	\N	\N
1017	Moteles	moteles que en la misma ubicación física ofrecen uno o más servicios integrados bajo la misma razón social, alojamiento temporal en, moteles sin otros servicios integrados, alojamiento temporal en	t	\N	\N
1018	Hoteles con casino	alojamiento temporal en combinación con servicios de casino, hoteles con casino	t	\N	\N
1019	Cabañas, villas y similares	alojamiento temporal mediante la modalidad de tiempos compartidos en bungalows, alojamiento temporal mediante la modalidad de tiempos compartidos en cabañas, alojamiento temporal mediante la modalidad de tiempos compartidos en villas, bungalows, alojamiento temporal en, cabañas, alojamiento temporal en, casas típicas para viajeros, alojamiento temporal en, hostales, alojamiento temporal en, hoteles que sin ser campamentos o albergues sólo atienden a jóvenes, alojamiento temporal en, villas, aloj	t	\N	\N
1020	Campamentos y albergues recreativos	albergues juveniles, alojamiento temporal en, albergues recreativos, alojamiento temporal en, campamentos de montaña, alojamiento temporal en, campamentos para caza y pesca, alojamiento temporal en, campamentos que reciben casas rodantes (trailer parks), alojamiento temporal en, campamentos recreativos con pernoctación, alojamiento temporal en, espacios para casas móviles y tiendas de campaña, alojamiento temporal en, habitaciones compartidas, alojamiento para viajeros en	t	\N	\N
1021	Pensiones y casas de huéspedes	casas de huéspedes, alojamiento temporal en, pensiones para huéspedes, alojamiento temporal en	t	\N	\N
1022	Departamentos y casas amueblados con servicios de hotelería	campamentos de trabajadores, alojamiento temporal en, casas amuebladas con servicios de hotelería, alojamiento temporal en, departamentos amueblados con servicios de hotelería, alojamiento temporal en	t	\N	\N
1023	Servicios de comedor para empresas e instituciones	alimentos para consumo inmediato por contrato para empresas e instituciones, preparación y entrega, alimentos y bebidas en abastecedoras por contrato para consumo inmediato para empresas e instituciones, preparación y entrega, alimentos y bebidas para consumo inmediato por contrato para escuelas, preparación y entrega, alimentos y bebidas para consumo inmediato por contrato para hospitales, preparación y entrega, alimentos y bebidas para consumo inmediato por contrato para industrias, preparació	t	\N	\N
1024	Servicios de preparación de alimentos para ocasiones especiales	alimentos y bebidas para bodas, preparación y entrega, alimentos y bebidas para conferencias, preparación y entrega, alimentos y bebidas para consumo inmediato para ocasiones especiales, preparación y entrega, alimentos y bebidas para seminarios, preparación y entrega, banquetes, servicios de, bufetes para ocasiones especiales, preparación de, preparación de alimentos y bebidas para ocasiones especiales en combinación con el alquiler de salones de fiestas	t	\N	\N
1025	Servicios de preparación de alimentos en unidades móviles	aguas frescas para consumo inmediato en unidades móviles, preparación de, alimentos y bebidas para consumo inmediato en carros móviles motorizados, preparación, alimentos y bebidas para consumo inmediato en carros móviles no motorizados, preparación, alimentos y bebidas para consumo inmediato en unidades móviles, preparación, antojitos para consumo inmediato en unidades móviles, preparación, atole para consumo inmediato en unidades móviles, preparación de, fruta para consumo inmediato en unidade	t	\N	\N
1026	Centros nocturnos, discotecas y similares	antros, preparación y servicio de bebidas alcohólicas, cabarets, preparación y servicio de bebidas alcohólicas, centros nocturnos, preparación y servicio de bebidas alcohólicas, cervezas preparadas y servidas o despachadas para consumo inmediato en centros nocturnos, discotecas y similares, discotecas, preparación y servicio de bebidas alcohólicas, licores preparados y servidos o despachados para consumo inmediato en centros nocturnos, discotecas y similares, preparación y servicio de bebidas al	t	\N	\N
1027	Bares, cantinas y similares	bares, preparación y servicio de bebidas alcohólicas para consumo inmediato, bebidas alcohólicas para consumo inmediato, preparación y servicio, cantinas, preparación y servicio de bebidas alcohólicas para consumo inmediato, cervecerías, preparación y servicio de bebidas alcohólicas para consumo inmediato, cervezas preparadas y servidas o despachadas para consumo inmediato en bares, cantinas y similares, licores preparados y servidos o despachados para consumo inmediato en bares, cantinas y simi	t	\N	\N
1028	Restaurantes con servicio de preparación de alimentos a la carta o de comida corrida	alimentos y bebidas a la carta para consumo inmediato en las instalaciones del restaurante, preparación de, cocinas económicas para consumo inmediato en las instalaciones del restaurante, preparación de alimentos y bebidas en, restaurantes con servicio de preparación de alimentos a la carta o de comida corrida, restaurantes de comida corrida, preparación de alimentos y bebidas en	t	\N	\N
1029	Restaurantes con servicio de preparación de pescados y mariscos	marisquerías para consumo inmediato en las instalaciones del restaurante, preparación de alimentos y bebidas en, ostionerías para consumo inmediato en las instalaciones del restaurante, preparación de alimentos y bebidas en, restaurantes con servicio de preparación de pescados y mariscos	t	\N	\N
1030	Restaurantes con servicio de preparación de antojitos	antojerías para consumo inmediato en las instalaciones del restaurante, preparación de alimentos y bebidas en, birria para consumo inmediato en las instalaciones del restaurante, preparación de, birrierías para consumo inmediato en las instalaciones del restaurante, preparación de alimentos y bebidas en, gorditas para consumo inmediato en las instalaciones del restaurante, preparación de alimentos y bebidas en, menudo para consumo inmediato en las instalaciones del restaurante, preparación de, p	t	\N	\N
1031	Restaurantes con servicio de preparación de tacos y tortas	hamburguesas para consumo inmediato en las instalaciones del restaurante, preparación de, hot dogs para consumo inmediato en las instalaciones del restaurante, preparación de, restaurantes con servicio de preparación de tacos y tortas, sándwiches para consumo inmediato en las instalaciones del restaurante, preparación de, taquerías para consumo inmediato en las instalaciones del restaurante, preparación de alimentos y bebidas en, torterías para consumo inmediato en las instalaciones del restaura	t	\N	\N
1032	Cafeterías, fuentes de sodas, neverías, refresquerías y similares	bebidas no alcohólicas (café, té, chocolate) para consumo inmediato en combinación con la elaboración de pan, preparación de, café para consumo inmediato en combinación con el tostado y la molienda del mismo, preparación de, café para llevar o de autoservicio, preparación, cafeterías para consumo inmediato en las instalaciones de la unidad económica, preparación de alimentos y bebidas en, cafeterías, fuentes de sodas, neverías, refresquerías y similares, fuentes de sodas para consumo inmediato e	t	\N	\N
1033	Restaurantes de autoservicio	alimentos y bebidas para consumo inmediato por ventanilla de servicio al automóvil, preparación, cafeterías de autoservicio, preparación de alimentos y bebidas en, neverías de autoservicio, preparación de alimentos y bebidas en, pizzerías de autoservicio, preparación de alimentos y bebidas en, restaurantes bufete, preparación de alimentos y bebidas en, restaurantes de autoservicio, restaurantes de autoservicio donde el cliente ordena desde su auto, preparación de alimentos y bebidas en, restaura	t	\N	\N
1034	Restaurantes con servicio de preparación de pizzas, hamburguesas, hot dogs y pollos rostizados para llevar	pizzerías de comida para llevar, preparación de alimentos y bebidas en, pollos adobados para llevar, preparación de, pollos asados para llevar, preparación de, restaurantes con servicio de preparación de pizzas, hamburguesas, hot dogs y pollos rostizados para llevar, rosticerías de comida para llevar, preparación de alimentos y bebidas en	t	\N	\N
1035	Restaurantes que preparan otro tipo de alimentos para llevar	aguas de frutas para llevar, preparación de, alimentos y bebidas a la carta para llevar, preparación de, antojerías de comida para llevar, preparación de alimentos y bebidas en, birrierías de comida para llevar, preparación de alimentos y bebidas en, cocinas económicas de comida para llevar, preparación de alimentos y bebidas en, fuente de sodas con bebidas para llevar, preparación de alimentos y bebidas en, jugos de frutas naturales para llevar, preparación de, pozolerías de comida para llevar,	t	\N	\N
1036	Servicios de preparación de otros alimentos para consumo inmediato	bebidas regionales no alcohólicas para su consumo inmediato en el mismo lugar o para llevar, preparación de, elotes para su consumo inmediato en el mismo lugar o para llevar, preparación de, frituras para su consumo inmediato en el mismo lugar o para llevar, preparación de, gelatinas para su consumo inmediato en el mismo lugar o para llevar, preparación de, pan casero para su consumo inmediato en el mismo lugar o para llevar, preparación de, pasteles para su consumo inmediato en el mismo lugar o	t	\N	\N
1037	Reparación mecánica en general de automóviles y camiones	automóviles y camiones en talleres de mecánica en general, afinación, automóviles y camiones, mantenimiento preventivo en talleres de mecánica en general, automóviles y camiones, reparación mecánica en general, escapes de automóviles y camiones en talleres de mecánica en general, reparación, frenos de automóviles y camiones en talleres de mecánica en general, reparación, motores de automóviles y camiones en talleres de mecánica en general, ajuste, radiadores de automóviles y camiones en talleres	t	\N	\N
1038	Reparación del sistema eléctrico y electrónico de automóviles y camiones	alternadores de automóviles y camiones, reparación eléctrica automotriz, baterías de automóviles y camiones, reparación eléctrica automotriz, luces de automóviles y camiones, reparación eléctrica automotriz, marchas de automóviles y camiones, reparación eléctrica automotriz, sistema de encendido de automóviles y camiones, reparación de, sistema de inyección de gasolina de automóviles y camiones, reparación de, sistema eléctrico de automóviles y camiones, reparación, sistema electrónico de automó	t	\N	\N
1039	Rectificación de partes de motor de automóviles y camiones	árbol de levas de automóviles y camiones, rectificación, automóviles y camiones, anillado, bielas de automóviles y camiones, rectificación, cabezas de motor de automóviles y camiones, rectificación, cigüeñales de automóviles y camiones, rectificación, monoblocks de automóviles y camiones, rectificación, partes de motores de automóviles a petición del cliente, rectificación, partes de motores de camiones a petición del cliente, rectificación, partes de motores, ajuste y recorte, pistones de autom	t	\N	\N
1040	Reparación de transmisiones de automóviles y camiones	direcciones hidráulicas de automóviles y camiones, reparación, transmisiones automáticas de automóviles y camiones, reparación, transmisiones estándar de automóviles y camiones, reparación, tren motriz de automóviles y camiones, reparación	t	\N	\N
1041	Reparación de suspensiones de automóviles y camiones	suspensiones de automóviles y camiones, reparación	t	\N	\N
1042	Alineación y balanceo de automóviles y camiones	automóviles y camiones, alineación, automóviles y camiones, balanceo, ejes traseros de automóviles y camiones, enderezamiento, ruedas de automóviles y camiones, reparación menor	t	\N	\N
1043	Otras reparaciones mecánicas de automóviles y camiones	amortiguadores de automóviles y camiones en talleres especializados, reparación de, automóviles y camiones en talleres especializados, afinación, carburadores de automóviles y camiones en talleres especializados, reparación, diagnósticos de fallas por computadora de automóviles y camiones en talleres especializados, embragues (clutch) de automóviles y camiones en talleres especializados, reparación, escapes de automóviles y camiones en talleres especializados, reparación, frenos de automóviles y	t	\N	\N
1044	Hojalatería y pintura de automóviles y camiones	automóviles antiguos y clásicos, restauración, automóviles y camiones, hojalatería, automóviles y camiones, pintura, automóviles y camiones, soldadura, carrocería de automóviles y camiones, reparación mayor, carrocería de automóviles y camiones, reparación menor, carrocerías de automóviles y camiones, adaptación, carrocerías de automóviles y camiones, conversión, chasises, postes y similares de automóviles y camiones, reparación, chasises, postes y similares de automóviles y camiones, enderezami	t	\N	\N
1045	Tapicería de automóviles y camiones	alfombras para automóviles y camiones, reparación, automóviles y camiones, tapicería, capotas, reparación, tapices para automóviles y camiones, reparación, tapices para interiores de automóviles y camiones, revestimiento	t	\N	\N
1046	Servicios de blindaje y de adaptación de automóviles y camiones	adaptación de automóviles y camiones para usos especiales a petición del cliente, servicios de, adaptación de vehículos para personas con discapacidad, servicios de, adaptación de vehículos para servicio de alimentos, servicios de, blindaje de vehículos a petición del cliente, servicios de	t	\N	\N
1047	Instalación de cristales y otras reparaciones a la carrocería de automóviles y camiones	campers de fibra de vidrio de automóviles y camiones, reparación, carrocería de automóviles y camiones, reparación, cristales de automóviles y camiones, instalación, cristales de automóviles y camiones, sustitución y reparación, elevadores automotrices, reparación, limpiaparabrisas de automóviles y camiones, reparación, remolques para botes y casas rodantes, reparación y mantenimiento	t	\N	\N
1048	Reparación menor de llantas	cámaras de llantas con parche caliente, reparación, cámaras de llantas con parche frío, reparación, cámaras de llantas de automóviles y camiones, reparación menor, llantas con parche frío, reparación, llantas con parches radiales, reparación, llantas de automóviles y camiones, reparación menor, vulcanizadoras (reparación menor de llantas y cámaras)	t	\N	\N
1049	Lavado y lubricado de automóviles y camiones	autolavados, servicios de, automóviles y camiones, encerado, automóviles y camiones, lavado, automóviles y camiones, lubricado, automóviles y camiones, pulido, carrocerías, lavado, chasis, lavado, lavado de interiores de automóviles y camiones, motores de automóviles y camiones, lavado	t	\N	\N
1050	Otros servicios de reparación y mantenimiento de automóviles y camiones	autoestéreos y accesorios de automóviles y camiones, instalación, automóviles y camiones, impermeabilización, automóviles y camiones, verificación vehicular, cambio de aceite, servicio automotriz de, climas automotrices, instalación y reparación, cristales para automóviles y camiones, polarizado, equipo de sonido para automóviles, instalación, recubrimientos antioxidantes para automóviles y camiones, instalación, sistemas de aire acondicionado automotrices, instalación y reparación, sistemas de 	t	\N	\N
1051	Reparación y mantenimiento de equipo electrónico de uso doméstico	Blu-ray, reparación y mantenimiento, bocinas de uso doméstico, reparación y mantenimiento, cámaras de video de uso doméstico, reparación y mantenimiento, cámaras y equipo fotográfico de uso doméstico, reparación y mantenimiento, equipos modulares de uso doméstico, reparación y mantenimiento, equipos reproductores de discos compactos (CD) de uso doméstico, reparación y mantenimiento, equipos reproductores de discos de video digital (DVD) de uso doméstico, reparación y mantenimiento, grabadoras de	t	\N	\N
1052	Reparación y mantenimiento de otro equipo electrónico y de equipo de precisión	aparatos de rayos x, reparación y mantenimiento, aparatos e instrumentos para medir ángulos, distancias e inclinaciones de terrenos, reparación y mantenimiento, aparatos e instrumentos para medir fenómenos meteorológicos, reparación y mantenimiento, aparatos e instrumentos para medir longitudes y diámetros, reparación y mantenimiento, aparatos e instrumentos para medir y verificar magnitudes, reparación y mantenimiento, aspiradoras médicas de flemas, reparación y mantenimiento, autoclaves, repar	t	\N	\N
1053	Reparación y mantenimiento de maquinaria y equipo agropecuario y forestal	arados, reparación y mantenimiento, aspersores, reparación y mantenimiento, cortadoras, reparación y mantenimiento, cosechadoras, reparación y mantenimiento, cribadoras, reparación y mantenimiento, cuchillas, reparación y mantenimiento, desmenuzadoras, reparación y mantenimiento, incubadoras, reparación y mantenimiento, maquinaria y equipo agropecuario, limpieza, maquinaria y equipo agropecuario, reparación y mantenimiento, maquinaria y equipo forestal, limpieza, maquinaria y equipo forestal, re	t	\N	\N
1054	Reparación y mantenimiento de maquinaria y equipo industrial	andamios, reparación y mantenimiento, bombas de uso industrial, reparación y mantenimiento, calderas generadoras de vapor, reparación y mantenimiento, cojinetes metálicos de uso industrial, reparación y mantenimiento, compresoras industriales, reparación y mantenimiento, cortinas metálicas en general, reparación y mantenimiento, engranajes para equipo industrial, reparación y mantenimiento, equipo de soldadura autógena, reparación y mantenimiento, equipo de transmisión de energía eléctrica, repa	t	\N	\N
1055	Reparación y mantenimiento de maquinaria y equipo para mover, levantar y acomodar materiales	cargadores frontales, reparación y mantenimiento, contenedores, limpieza y reparación, elevadores de todo tipo, reparación y mantenimiento, equipos transportadores de acción continua, reparación y mantenimiento, escaleras eléctricas, reparación y mantenimiento, gatos hidráulicos, reparación y mantenimiento, grúas en general, reparación y mantenimiento, maquinaria y equipo para mover, levantar y acomodar materiales, reparación y mantenimiento, montacargas, reparación y mantenimiento, tarimas para	t	\N	\N
1056	Reparación y mantenimiento de maquinaria y equipo comercial y de servicios	bombas para estación de servicio, reparación y mantenimiento, cámaras frigoríficas, reparación y mantenimiento, canceles, reparación y mantenimiento, equipo audiovisual para el comercio y los servicios, reparación y mantenimiento, equipo de refrigeración comercial, reparación y mantenimiento, equipo para electrolineras, reparación de, equipo para salones de belleza, reparación y mantenimiento, lonas para uso comercial y de servicios, reparación, maquinaria y equipo comercial, limpieza, maquinari	t	\N	\N
1057	Reparación y mantenimiento de aparatos eléctricos para el hogar y personales	aparatos eléctricos para el hogar, reparación y mantenimiento, aparatos eléctricos personales, reparación y mantenimiento, asadores eléctricos para el hogar, reparación y mantenimiento, aspiradoras para el hogar, reparación y mantenimiento, batidoras para el hogar, reparación y mantenimiento, cafeteras para el hogar, reparación y mantenimiento, calentadores eléctricos para el hogar, reparación y mantenimiento, campanas purificadoras para el hogar, reparación y mantenimiento, cobertores eléctrico	t	\N	\N
1058	Reparación de tapicería de muebles para el hogar	alfombras para el hogar, reparación, colchones para el hogar, reparación, muebles para el hogar, reparación, muebles para el hogar, tapicería, tapetes para el hogar, reparación, tapicería de muebles para el hogar, reparación, tapicería de sillas para el hogar, reparación, tapicería de sillones para el hogar, reparación, tapicería de sofás para el hogar, reparación	t	\N	\N
1059	Reparación de calzado y otros artículos de piel y cuero	artículos de piel o cuero, reparación, artículos de talabartería, reparación, bolsos de mano de piel o cuero, reparación, calzado, remodelación, calzado, reparación y mantenimiento, chamarras de piel o cuero, reparación, guantes de piel o cuero, reparación, hormas para calzado, ajustamiento, maletas de piel o cuero, reparación, mochilas de piel o cuero, reparación, portafolios de piel o cuero, reparación, ropa de piel o cuero, reparación, suelas para calzado, reparación, tacones para calzado, re	t	\N	\N
1060	Cerrajerías	apertura de cerraduras combinada con su reparación, apertura de cerraduras de cajas fuertes, apertura de cerraduras de muebles, apertura de cerraduras de puertas, cajas fuertes, reparación de cerraduras de, cambio de cerraduras de cajas fuertes, cambio de cerraduras de muebles, cambio de cerraduras de puertas, candados, reparación, cerraduras de puertas, reparación, cerrajerías, servicios de, duplicado de llaves en combinación con la apertura o reparación de cerraduras, llaves, duplicado de, mue	t	\N	\N
1061	Reparación y mantenimiento de motocicletas	cuatrimotos, reparación y mantenimiento, motocicletas, reparación y mantenimiento, motonetas, reparación y mantenimiento, talleres de reparación de motocicletas, servicios de, tricimotos, reparación y mantenimiento	t	\N	\N
1062	Reparación y mantenimiento de bicicletas	bicicletas, reparación y mantenimiento, cuadriciclos, reparación y mantenimiento, talleres de reparación de bicicletas, servicios de, triciclos, reparación y mantenimiento	t	\N	\N
1063	Reparación y mantenimiento de otros artículos para el hogar y personales	anteojos, reparación de, aparatos de gimnasia, reparación y mantenimiento, armas de fuego para deporte y caza, reparación, artículos de plata, limpieza, artículos para el hogar, soldadura, bastones, reparación, calentadores solares para agua, reparación, celosías, reparación, cuchillos para el hogar, afilado, embarcaciones recreativas (excepto yates que requieren tripulación), reparación, mantenimiento y modificación, equipo para actividades deportivas y recreativas, reparación y mantenimiento, 	t	\N	\N
1064	Salones y clínicas de belleza y peluquerías	afeitado, servicios de, alaciado de cabello, aplicación de mascarillas y vendas, aplicación de tatuajes corporales, aplicación de uñas postizas, bronceado corporal, servicios de, centros de masaje, servicios de, clínicas de belleza, servicios de, clínicas de depilación, servicios de, coloración y teñido del cabello, corte de cabello, cuidado de la piel, cuidado de uñas, cuidado del cabello, cuidado y arreglo personal, servicios de, decoloración del cabello, depilado permanente, depilado temporal	t	\N	\N
1065	Baños públicos	baños de hidromasaje, servicios de, baños de vapor, servicios de, baños públicos, servicios de, baños turcos, servicios de, regaderas, servicios de, sauna, servicios de, solarios, servicios de	t	\N	\N
1067	Lavanderías y tintorerías	acceso a máquinas de lavandería, artículos de cuero, limpieza, artículos de piel, limpieza, lavandería comercial, servicios de, lavandería en combinación con el alquiler de uniformes, blancos y pañales, lavandería industrial, servicios de, lavandería para el consumidor (excepto lavanderías comerciales), servicios de, lavandería y tintorería por agentes intermediarios, servicios de, planchado, servicios de, ropa, desmanchado de, ropa, lavado de, ropa, teñido en lavanderías o tintorerías, tintorer	t	\N	\N
1068	Servicios funerarios	agencias funerarias, agencias funerarias que combinan su actividad con el comercio de ataúdes, aquamación, servicios de, capillas de velación, servicios de, cremación de restos humanos, embalsamamiento de humanos, servicios de, entierro de restos humanos, servicios funerarios integrales para humanos (en paquete), servicios funerarios para humanos, servicios funerarios para humanos, planeación y coordinación de, transporte foráneo de restos humanos, transporte local de restos humanos, traslado fo	t	\N	\N
1069	Administración de cementerios pertenecientes al sector privado	cementerios del sector privado para humanos, administración de, cementerios del sector privado para humanos, conservación y mantenimiento, cementerios del sector privado para humanos, vigilancia de, espacios para la disposición final de restos humanos en cementerios del sector privado, alquiler de, espacios para la disposición final de restos humanos en cementerios del sector privado, venta de, exhumación de restos humanos en cementerios del sector privado, servicios de, inhumación de restos hum	t	\N	\N
1070	Administración de cementerios pertenecientes al sector público	cementerios del sector público para humanos, administración de, cementerios del sector público para humanos, conservación y mantenimiento, cementerios del sector público para humanos, vigilancia de, espacios para la disposición final de restos humanos en cementerios del sector público, alquiler de, espacios para la disposición final de restos humanos en cementerios del sector público, venta de, exhumación de restos humanos en cementerios del sector público, servicios de, inhumación de restos hum	t	\N	\N
1071	Estacionamientos y pensiones para vehículos automotores	administración de parquímetros, estacionamiento asistido por personal (valet parking), estacionamiento en inmuebles por semana o mes, estacionamiento en la vía pública, servicios de, estacionamiento en lugares diferentes a la vía pública por hora o día, servicios de, estacionamiento en terrenos por semana o mes, servicios de, estacionamiento para vehículos automotores, estacionamientos públicos, servicios de, pensión para vehículos automotores	t	\N	\N
1072	Servicios de revelado e impresión de fotografías	ampliación de fotografías, autoservicio de impresión de fotografías en máquinas automáticas, impresión de fotografías, reducción de fotografías, restauración digital de fotografías, revelado de fotografías, revelado de fotografías comerciales y de negocios, revelado de fotografías en una hora, revelado de fotografías para el día siguiente, revelado e impresión de fotografías en combinación con el comercio de artículos fotográficos	t	\N	\N
1073	Otros servicios personales	adiestramiento de perros guía, agencias matrimoniales, arreglo de mascotas, aseo para mascotas, astrología, servicios de, brujos, servicios de, cartomancia, servicios de, casilleros (lockers) que funcionan con monedas, servicios de, cementerios para mascotas, administración de, cementerios para mascotas, conservación y mantenimiento, cementerios para mascotas, vigilancia de, corte de pelo y uñas para mascotas, cremación de restos de mascotas, cuidado de mascotas (excepto cuidados veterinarios), 	t	\N	\N
1074	Asociaciones, organizaciones y cámaras de productores, comerciantes y prestadores de servicios	asociaciones de comerciantes, asociaciones de prestadores de servicios, asociaciones de productores agrícolas, asociaciones de productores industriales	t	\N	\N
1075	Asociaciones y organizaciones laborales y sindicales	asociaciones laborales, asociaciones sindicales, sindicatos	t	\N	\N
1076	Asociaciones y organizaciones de profesionistas	asociaciones de abogados, asociaciones de arquitectos, asociaciones de artistas, asociaciones de deportistas, asociaciones de ingenieros, asociaciones de médicos, asociaciones de profesionistas	t	\N	\N
1077	Asociaciones regulatorias de actividades recreativas	asociaciones regulatorias de actividades recreativas, federaciones de atletismo, federaciones de básquetbol, federaciones de béisbol, federaciones de ciclismo, federaciones de esgrima, federaciones de futbol, federaciones de gimnasia, federaciones de golf, federaciones de natación, federaciones de tenis, federaciones de voleibol, federaciones deportivas	t	\N	\N
1078	Asociaciones y organizaciones religiosas	asociaciones eclesiásticas, asociaciones religiosas, basílicas, servicios religiosos, capillas, servicios religiosos, casas de retiro, servicios religiosos, catedrales, servicios religiosos, centros de servicios misioneros, servicios religiosos, congregaciones de misioneros, servicios religiosos, conventos, servicios religiosos, iglesias, servicios religiosos, institutos bíblicos, servicios religiosos, institutos ecuménicos, servicios religiosos, mezquitas, servicios religiosos, monasterios, ser	t	\N	\N
1079	Asociaciones y organizaciones políticas	asociaciones políticas, organizaciones políticas, partidos políticos	t	\N	\N
1080	Asociaciones y organizaciones civiles	asociaciones civiles, asociaciones civiles de caridad, asociaciones civiles de cultura, asociaciones civiles de derechos de los colonos, asociaciones civiles de derechos humanos, asociaciones civiles de educación, asociaciones civiles de protección al medio ambiente, asociaciones civiles de salud, asociaciones civiles de seguridad de la comunidad, asociaciones de alumnos, asociaciones de automovilistas, asociaciones de condóminos, asociaciones de estudiantes, asociaciones de padres de familia, a	t	\N	\N
1081	Hogares con empleados domésticos	hogares que emplean amas de llaves, hogares que emplean camaristas, hogares que emplean choferes, hogares que emplean cocineros, hogares que emplean cuidadores de ancianos, hogares que emplean cuidadores de niños, hogares que emplean cuidadores de personas con discapacidad, hogares que emplean jardineros, hogares que emplean lavanderos, hogares que emplean mayordomos, hogares que emplean mozos, hogares que emplean personal doméstico, hogares que emplean planchadores, hogares que emplean porteros	t	\N	\N
1082	Órganos legislativos	Asamblea de representantes, servicios de, Cámara de diputados, servicios de, Cámara de senadores, servicios de	t	\N	\N
1083	Administración pública en general	administración de la deuda pública estatal, administración de la deuda pública federal, administración de la deuda pública municipal, administración pública estatal de asuntos financieros, administración pública estatal de asuntos fiscales, administración pública estatal de la recaudación fiscal, administración pública estatal en general, administración pública federal de aduanas, administración pública federal de asuntos financieros, administración pública federal de asuntos fiscales, administr	t	\N	\N
1084	Regulación y fomento del desarrollo económico	administración estatal de actividades económicas estratégicas, administración estatal de comunicaciones y transportes, administración estatal de fondos para el desarrollo económico, administración estatal de lucha contra las plagas, administración estatal de ordenación de tierras de uso agropecuario, administración federal de actividades económicas estratégicas, administración federal de comunicaciones y transportes, administración federal de fondos para el desarrollo económico, administración f	t	\N	\N
1085	Impartición de justicia	administración estatal de justicia mediante juzgados y tribunales, administración estatal del sistema judicial, administración federal de justicia mediante juzgados y tribunales, administración federal del sistema judicial, administración municipal de justicia mediante juzgados y tribunales, administración municipal del sistema judicial, servicio médico forense estatal, servicio médico forense federal, servicio médico forense municipal, tribunales de lo contencioso administrativo, consejos de la	t	\N	\N
1086	Mantenimiento de la seguridad y el orden público	administración estatal de cuerpos policiacos, administración federal de cuerpos policiacos, administración municipal de cuerpos policiacos, centros de detención migratoria, administración federal de, centros de detención penal, administración municipal de, centros de readaptación social, administración estatal de, centros de readaptación social, administración federal de, centros de readaptación social, administración municipal de, combate y extinción de incendios por unidades gubernamentales, c	t	\N	\N
1087	Regulación y fomento de actividades para mejorar y preservar el medio ambiente	administración y regulación estatal de programas de protección ambiental, administración y regulación estatal de programas para el manejo de residuos, administración y regulación federal de programas de protección ambiental, administración y regulación federal de programas para el manejo de residuos, administración y regulación municipal de programas de protección ambiental, administración y regulación municipal de programas para el manejo de residuos, establecimiento de normas y procedimientos 	t	\N	\N
1088	Actividades administrativas de instituciones de bienestar social	actividades administrativas de instituciones estatales de bienestar social, actividades administrativas de instituciones estatales para la investigación y desarrollo científicos, actividades administrativas de instituciones estatales para la regulación de asuntos laborales, actividades administrativas de instituciones federales de bienestar social, actividades administrativas de instituciones federales para la investigación y desarrollo científicos, actividades administrativas de instituciones f	t	\N	\N
1089	Relaciones exteriores	administración de relaciones exteriores, embajadas de nuestro país en el extranjero, servicios de, establecimiento de relaciones diplomáticas entre México y organismos internacionales, sedes diplomáticas de nuestro país en el extranjero	t	\N	\N
1090	Actividades de seguridad nacional	ejército, servicios del, fuerza aérea, servicios de la, guardia nacional, servicios de la, marina, servicios de la, salvaguarda de la seguridad nacional por unidades gubernamentales	t	\N	\N
1091	Organismos internacionales	Centro de Estudios Monetarios Latinoamericanos (CEMLA), Comisión Económica para América Latina y el Caribe (CEPAL), organismos internacionales que brindan cooperación y apoyo económico, comercial y tecnológico, Organización de Estados Americanos (OEA), Organización de las Naciones Unidas (ONU), Organización de las Naciones Unidas para la Agricultura y la Alimentación (FAO), Organización Internacional del Trabajo (OIT), Organización para la Cooperación y el Desarrollo Económicos (OCDE)	t	\N	\N
1092	Sedes diplomáticas y otras unidades extraterritoriales	consulados con ubicación física en nuestro país, servicios de; embajadas con ubicación física en nuestro país, servicios de; sedes diplomáticas y otras unidades extraterritoriales con ubicación física en nuestro país; unidades militares que brindan apoyo en nuestro país	t	\N	\N
\.


--
-- Data for Name: dependency_resolutions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dependency_resolutions (id, procedure_id, role, user_id, resolution_status, resolution_text, resolution_file, signature, deleted_at, created_at, updated_at) FROM stdin;
16	1	1	\N	1	Resolución administrativa aprobada para el trámite PROC-001. Se autoriza el procedimiento solicitado conforme a la normativa vigente.	resolution_proc001_admin.pdf	admin_signature_001	\N	2024-01-15 09:00:00	2024-01-15 09:00:00
17	1	2	\N	1	Resolución directiva confirmando la aprobación del trámite PROC-001. Procede según lo establecido en el reglamento municipal.	resolution_proc001_director.pdf	director_signature_001	\N	2024-01-15 14:30:00	2024-01-15 14:30:00
18	1	3	\N	2	Observaciones técnicas sobre el trámite PROC-001. Se requieren ajustes menores en la documentación presentada.	resolution_proc001_tech.pdf	tech_signature_001	\N	2024-01-16 10:15:00	2024-01-17 16:45:00
19	2	1	\N	3	Resolución de rechazo para el trámite PROC-002. No cumple con los requisitos mínimos establecidos en el artículo 15 del reglamento.	resolution_proc002_rejected.pdf	admin_signature_002	\N	2024-01-18 11:20:00	2024-01-18 11:20:00
20	2	2	\N	3	Confirmación directiva del rechazo del trámite PROC-002. Se notifica al solicitante para subsanar las deficiencias identificadas.	resolution_proc002_director_reject.pdf	director_signature_002	\N	2024-01-19 08:45:00	2024-01-19 08:45:00
21	3	1	\N	4	Resolución en proceso de revisión para el trámite con folio string. Pendiente de validación técnica por parte del departamento especializado.	\N	\N	\N	2024-01-20 13:30:00	2024-01-22 09:15:00
22	3	3	\N	4	Evaluación técnica pendiente. Se requiere inspección en campo antes de emitir resolución definitiva.	\N	\N	\N	2024-01-21 15:00:00	2024-01-23 11:30:00
23	4	1	\N	5	Resolución aprobada con condiciones para PROC-004. Se autoriza con las restricciones especificadas en el anexo técnico adjunto.	resolution_proc004_conditional.pdf	admin_signature_004	\N	2024-01-24 10:00:00	2024-01-24 10:00:00
24	4	2	\N	5	Validación directiva de la aprobación condicional. El solicitante debe cumplir con las medidas correctivas en un plazo de 30 días.	resolution_proc004_director_conditional.pdf	director_signature_004	\N	2024-01-24 16:20:00	2024-01-24 16:20:00
25	5	1	\N	1	Resolución inicial aprobada para PROC-005. Autorización preliminar otorgada conforme a solicitud presentada.	resolution_proc005_initial.pdf	admin_signature_005_v1	\N	2024-01-25 09:30:00	2024-01-26 14:15:00
26	5	1	\N	2	Resolución modificada para PROC-005. Se requieren documentos adicionales antes de la autorización final.	resolution_proc005_modified.pdf	admin_signature_005_v2	\N	2024-01-26 14:15:00	2024-01-28 10:45:00
27	5	2	\N	1	Resolución directiva final para PROC-005. Aprobación definitiva tras cumplimiento de requisitos adicionales.	resolution_proc005_final.pdf	director_signature_005_final	\N	2024-01-28 10:45:00	2024-01-28 10:45:00
28	1	1	\N	1	Esta es una resolución con texto extenso para probar el manejo de contenido largo en el sistema. La resolución abarca múltiples aspectos técnicos, legales y administrativos que deben ser considerados en el proceso de evaluación. Se incluyen referencias a normativas municipales, estatales y federales aplicables al caso. Además, se especifican las condiciones particulares que debe cumplir el solicitante, los plazos establecidos para cada etapa del proceso, y las consecuencias del incumplimiento de cualquiera de las disposiciones establecidas en la presente resolución administrativa. La autoridad competente se reserva el derecho de realizar inspecciones periódicas para verificar el cumplimiento de todas las condiciones aquí establecidas.	resolution_long_text.pdf	signature_long_001	\N	2024-01-29 08:00:00	2024-01-29 08:00:00
29	2	3	\N	4	Resolución sin archivo adjunto para pruebas de campos opcionales. Esta resolución se encuentra en proceso de digitalización.	\N	\N	\N	2024-01-30 12:00:00	2024-01-30 12:00:00
30	3	2	\N	1	Resolución reciente para pruebas de ordenamiento por fecha. Esta es la resolución más actualizada en el sistema de pruebas.	resolution_recent.pdf	recent_signature	\N	2024-02-01 16:30:00	2024-02-01 16:30:00
\.


--
-- Data for Name: dependency_reviews; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dependency_reviews (id, procedure_id, municipality_id, folio, role, start_date, update_date, current_status, current_file, signature, user_id, created_at, updated_at) FROM stdin;
61	1	1	TEST-DR-001	1	2024-01-15 09:00:00	2024-01-15 09:00:00	1	file_001.pdf	signature_001	\N	2024-01-15 09:00:00	2024-01-15 09:00:00
62	2	1	TEST-DR-002	2	2024-01-16 10:30:00	2024-01-16 14:20:00	2	file_002.pdf	signature_002	\N	2024-01-16 10:30:00	2024-01-16 14:20:00
63	3	2	TEST-DR-003	1	2024-01-17 11:45:00	2024-01-17 16:15:00	3	file_003.pdf	signature_003	\N	2024-01-17 11:45:00	2024-01-17 16:15:00
64	1	2	TEST-DR-004	3	2024-01-18 08:20:00	2024-01-18 12:40:00	1	file_004.pdf	signature_004	\N	2024-01-18 08:20:00	2024-01-18 12:40:00
65	2	3	TEST-DR-005	2	2024-01-19 13:15:00	2024-01-19 17:30:00	2	file_005.pdf	signature_005	\N	2024-01-19 13:15:00	2024-01-19 17:30:00
66	1	1	TEST-DR-006	1	2024-02-01 09:00:00	2024-02-01 09:00:00	1	file_006.pdf	signature_006	\N	2024-02-01 09:00:00	2024-02-01 09:00:00
67	2	1	TEST-DR-007	2	2024-02-15 10:30:00	2024-02-15 14:20:00	2	file_007.pdf	signature_007	\N	2024-02-15 10:30:00	2024-02-15 14:20:00
68	3	2	TEST-DR-008	1	2024-03-01 11:45:00	2024-03-01 16:15:00	3	file_008.pdf	signature_008	\N	2024-03-01 11:45:00	2024-03-01 16:15:00
69	1	2	TEST-DR-009	3	2024-03-15 08:20:00	2024-03-15 12:40:00	1	file_009.pdf	signature_009	\N	2024-03-15 08:20:00	2024-03-15 12:40:00
70	2	3	TEST-DR-010	2	2024-04-01 13:15:00	2024-04-01 17:30:00	2	file_010.pdf	signature_010	\N	2024-04-01 13:15:00	2024-04-01 17:30:00
71	1	1	TEST-DR-011	1	2023-12-01 09:00:00	2023-12-01 09:00:00	1	file_011.pdf	signature_011	\N	2023-12-01 09:00:00	2023-12-01 09:00:00
72	2	1	TEST-DR-012	2	2023-12-15 10:30:00	2023-12-15 14:20:00	2	file_012.pdf	signature_012	\N	2023-12-15 10:30:00	2023-12-15 14:20:00
73	3	2	TEST-DR-013	1	2023-11-01 11:45:00	2023-11-01 16:15:00	3	file_013.pdf	signature_013	\N	2023-11-01 11:45:00	2023-11-01 16:15:00
74	1	2	TEST-DR-014	3	2023-11-15 08:20:00	2023-11-15 12:40:00	1	file_014.pdf	signature_014	\N	2023-11-15 08:20:00	2023-11-15 12:40:00
75	2	3	TEST-DR-015	2	2023-10-01 13:15:00	2023-10-01 17:30:00	2	file_015.pdf	signature_015	\N	2023-10-01 13:15:00	2023-10-01 17:30:00
76	1	1	TEST-DR-016	1	\N	\N	\N	\N	\N	\N	2024-05-01 09:00:00	2024-05-01 09:00:00
77	2	2	TEST-DR-017	2	2024-05-02 10:00:00	\N	1	file_017.pdf	\N	\N	2024-05-02 10:00:00	2024-05-02 10:00:00
78	1	19	TEST-DR-018	1	2024-05-03 08:00:00	2024-05-03 12:00:00	2	file_018.pdf	signature_018	\N	2024-05-03 08:00:00	2024-05-03 12:00:00
79	4	19	TEST-DR-019	3	2024-05-04 09:30:00	2024-05-04 15:45:00	3	file_019.pdf	signature_019	\N	2024-05-04 09:30:00	2024-05-04 15:45:00
80	5	1	TEST-DR-020	2	2024-05-05 11:00:00	2024-05-05 16:30:00	1	file_020.pdf	signature_020	\N	2024-05-05 11:00:00	2024-05-05 16:30:00
\.


--
-- Data for Name: dependency_revisions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.dependency_revisions (id, dependency_id, revision_notes, revised_at, created_at, updated_at) FROM stdin;
43	2	TEST-REV-001: Initial review - Documentation incomplete. Missing building permits and safety certificates.	2024-01-15 09:00:00	2024-01-15 09:00:00	2024-01-15 09:00:00
44	2	TEST-REV-002: Second review - Building permits submitted but safety certificates still pending. Fire department approval required.	2024-01-22 14:30:00	2024-01-22 14:30:00	2024-01-22 14:30:00
45	2	TEST-REV-003: Third review - All documents submitted. Technical review in progress. Minor corrections needed in structural plans.	2024-01-29 11:15:00	2024-01-29 11:15:00	2024-01-29 11:15:00
46	2	TEST-REV-004: Final review - All requirements met. Approved for next phase. License ready for issuance.	2024-02-05 16:45:00	2024-02-05 16:45:00	2024-02-05 16:45:00
47	3	TEST-REV-005: Environmental impact assessment required. Property located near protected wetlands. Additional studies needed.	2024-01-18 10:20:00	2024-01-18 10:20:00	2024-01-18 10:20:00
48	3	TEST-REV-006: Environmental studies submitted. Mitigation plan approved. Proceed with standard review process.	2024-02-01 13:45:00	2024-02-01 13:45:00	2024-02-01 13:45:00
49	4	TEST-REV-007: Zoning compliance review - Current zoning allows commercial use but density restrictions apply. Variance may be required.	2024-01-20 08:30:00	2024-01-20 08:30:00	2024-01-20 08:30:00
50	4	TEST-REV-008: Zoning variance approved. Parking requirements modified. Additional landscaping required along street frontage.	2024-02-03 15:20:00	2024-02-03 15:20:00	2024-02-03 15:20:00
51	5	TEST-REV-009: Technical review - HVAC system specifications do not meet current building codes. Updated plans required.	2024-01-25 12:10:00	2024-01-25 12:10:00	2024-01-25 12:10:00
52	5	TEST-REV-010: Electrical system review - Load calculations incorrect. Professional engineer certification required.	2024-01-30 09:45:00	2024-01-30 09:45:00	2024-01-30 09:45:00
53	2	TEST-REV-011: Post-approval revision - Minor modification to façade design. Does not affect structural integrity.	2024-02-10 14:00:00	2024-02-10 14:00:00	2024-02-10 14:00:00
54	3	TEST-REV-012: Compliance check - Site inspection completed. All requirements met according to approved plans.	2024-02-08 11:30:00	2024-02-08 11:30:00	2024-02-08 11:30:00
55	4	TEST-REV-013: Amendment request - Business scope expansion requires additional review. New SCIAN classification needed.	2024-02-12 16:15:00	2024-02-12 16:15:00	2024-02-12 16:15:00
56	5	TEST-REV-014: Emergency revision - Code violation reported. Immediate compliance required for safety systems.	2024-02-15 08:00:00	2024-02-15 08:00:00	2024-02-15 08:00:00
57	2	TEST-REV-015: Historical revision - Legacy system migration. Previous approvals verified and documented.	2023-12-01 10:00:00	2023-12-01 10:00:00	2023-12-01 10:00:00
58	3	TEST-REV-016: Annual review - Periodic compliance check. All permits current and valid.	2023-11-15 14:30:00	2023-11-15 14:30:00	2023-11-15 14:30:00
59	4	TEST-REV-017: Current revision - New accessibility requirements. ADA compliance assessment in progress.	2024-06-01 09:15:00	2024-06-01 09:15:00	2024-06-01 09:15:00
60	5	TEST-REV-018: Latest revision - Digital submission review. Electronic documents verified and accepted.	2024-06-01 15:45:00	2024-06-01 15:45:00	2024-06-01 15:45:00
61	2	TEST-REV-019: Special characters test - Revisión con caracteres especiales: ñáéíóú. Review completed successfully.	2024-05-28 12:00:00	2024-05-28 12:00:00	2024-05-28 12:00:00
62	3	TEST-REV-020: Long note test - This is a very long revision note intended to test the system handling of extensive text content. It includes multiple sentences and various punctuation marks to ensure proper storage and retrieval.	2024-05-30 17:30:00	2024-05-30 17:30:00	2024-05-30 17:30:00
63	4	\N	2024-05-25 10:45:00	2024-05-25 10:45:00	2024-05-25 10:45:00
64	5		2024-05-26 13:20:00	2024-05-26 13:20:00	2024-05-26 13:20:00
\.


--
-- Data for Name: economic_activity_base; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.economic_activity_base (id, name) FROM stdin;
\.


--
-- Data for Name: economic_activity_sector; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.economic_activity_sector (id, name) FROM stdin;
\.


--
-- Data for Name: economic_supports; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.economic_supports (id, dependency, scian, program_name, url, program_description, deleted_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: economic_units_directory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.economic_units_directory (id, directory_type, commercial_name, legal_name, economic_activity_name, employed_people, road_type, road_name, road_type_ext_1, road_name_ext_1, road_type_ext_2, road_name_ext_2, road_type_ext_3, road_name_ext_3, exterior_number, exterior_letter, building, building_level, interior_number, interior_letter, settlement_type, settlement_name, mall_type, mall_name, local_number, postal_code, municipality_name, ageb, block, phone, email, website, registration_date, edited, economic_activity_id, locality_id, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: fields; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.fields (id, name, type, description, description_rec, rationale, options, options_description, step, sequence, required, visible_condition, affected_field, procedure_type, dependency_condition, trade_condition, status, municipality_id, editable, static_field, created_at, updated_at, deleted_at, required_official) FROM stdin;
\.


--
-- Data for Name: historical_procedures; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.historical_procedures (id, folio, current_step, user_signature, user_id, window_user_id, entry_role, documents_submission_date, procedure_start_date, window_seen_date, license_delivered_date, has_signature, no_signature_date, official_applicant_name, responsibility_letter, sent_to_reviewers, sent_to_reviewers_date, license_pdf, payment_order, status, step_one, step_two, step_three, step_four, director_approval, created_at, updated_at, window_license_generated, procedure_type, license_status, reason, renewed_folio, requirements_query_id) FROM stdin;
7	HIST-001	4	user_signature_data_hist_1	1	2	1	2023-05-31 15:58:23.030997	2023-05-31 15:58:23.030997	2023-06-05 15:58:23.030997	2023-06-30 15:58:23.030997	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	2	\N	\N	\N	\N	0	2025-05-31 15:58:23.030997	2025-05-31 15:58:23.030997	0	licencia_construccion	completado	\N	\N	\N
8	HIST-002	4	user_signature_data_hist_2	2	3	1	2024-05-31 15:58:23.030997	2024-05-31 15:58:23.030997	2024-06-05 15:58:23.030997	2024-06-30 15:58:23.030997	1	\N	María González	\N	\N	\N	\N	/uploads/payment_orders/order_hist_002.pdf	2	\N	\N	\N	\N	0	2025-05-31 15:58:23.030997	2025-05-31 15:58:23.030997	0	licencia_comercial	completado	\N	\N	\N
9	HIST-003	2	user_signature_data_hist_3	3	4	1	2023-11-30 15:58:23.030997	2023-11-30 15:58:23.030997	2023-12-05 15:58:23.030997	\N	1	\N	Carlos Rodríguez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_003.pdf	3	\N	\N	\N	\N	0	2025-05-31 15:58:23.030997	2025-05-31 15:58:23.030997	0	licencia_construccion	rechazado	\N	\N	\N
\.


--
-- Data for Name: inactive_businesses; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.inactive_businesses (id, business_line_id, municipality_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: issue_resolutions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.issue_resolutions (id, id_tramite, rol, id_usuario, comentario, comentario_usuario, archivos, fecha_maxima_solventacion, fecha_ingreso_documentos, fecha_visto, deleted_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: land_parcel_mapping; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.land_parcel_mapping (id, area_m2, "time", source, neighborhood_id, locality_id, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: map_layers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.map_layers (id, value, label, type, url, layers, visible, active, attribution, opacity, server_type, projection, version, format, "order", editable, type_geom, cql_filter) FROM stdin;
1	catastro_urbano	Capa de Catastro Urbano	WMS	https://visorurbano.gob.mx/geoserver/wms	VUJ:predios_urbanos	t	t	Visor Urbano	0.80	geoserver	EPSG:4326	1.3.0	image/png	1	t	polygon	INCLUDE
2	catastro_urbano	Capa de Catastro Urbano	WMS	https://datahub.mpiochih.gob.mx	VUJ:predios_urbanos	t	t	Visor Urbano	0.80	geoserver	EPSG:4326	1.3.0	image/png	1	t	polygon	INCLUDE
\.


--
-- Data for Name: maplayer_municipality; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.maplayer_municipality (maplayer_id, municipality_id) FROM stdin;
1	1
2	19
\.


--
-- Data for Name: municipalities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.municipalities (id, name, image, director, director_signature, process_sheet, solving_days, issue_license, address, phone, responsible_area, created_at, updated_at, deleted_at, window_license_generation, license_restrictions, license_price, initial_folio, has_zoning) FROM stdin;
1	string	string	string	string	1	0	0	string	string	string	2025-03-10 22:18:51.376612	2025-03-10 22:18:51.376612	\N	0		string	0	\N
19	Ayuntamiento Punta Cana	/images/ayuntamiento.png	Juan Perez	/signatures/juan_perez.png	1	30	0	Calle Falsa 123, Santo Domingo, Distrito Nacional	8091234567	Departamento de Gestión	\N	\N	\N	\N	\N	$100	1	\N
3	Tlaquepaque	https://example.com/tlaquepaque.jpg	Carlos Ruiz Mendoza	\N	1	12	1	Av. Revolución 115	33-5555-5555	Urbanismo y Obras Públicas	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	\N	\N	\N	\N	\N	\N
2	Chihuahua	/images/ayuntamiento.png	Juan Perez	/signatures/juan_perez.png	1	30	0	Calle Falsa 123, Santo Domingo, Distrito Nacional	8091234567	Departamento de Gestión	\N	2025-06-02 13:07:55.957142	\N	\N	\N	$100	1	t
\.


--
-- Data for Name: municipality_geoms; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.municipality_geoms (id, municipality_id, name, geom_type, coordinates, created_at, updated_at) FROM stdin;
1	2	Municipality 2	Polygon	[[[381010.5544004806, 3295344.9501948184], [383879.440900454, 3293858.15319479], [383953.7020004322, 3293761.4491947885], [384090.7772004276, 3293722.557294786], [384454.4509004486, 3293607.5418947786], [387856.8553004543, 3292531.627994764], [389137.2490004493, 3292142.0860947594], [390132.7096004416, 3291831.2705947496], [390888.24920044374, 3291619.4152947464], [391045.3828003969, 3291587.1884947475], [392060.86690044816, 3291290.74889474], [393249.3587004507, 3290921.365294732], [393302.8157004535, 3290904.751394731], [393295.28590041026, 3291281.527894735], [394027.73410040664, 3291314.5212947405], [394725.1338004647, 3291356.7689947356], [396321.67710043176, 3291459.1999947447], [397820.13550043514, 3291556.808694745], [400802.828700392, 3291774.589194752], [400912.5334003777, 3291780.2895947536], [401731.5199003936, 3291822.5533947544], [403272.02350037685, 3291907.280294754], [404422.60570040625, 3291979.2460947535], [404913.3249004041, 3292008.723094754], [406386.6859003485, 3292105.228494756], [408729.70120035554, 3292253.6297947587], [410184.6427003427, 3292295.3556947643], [409887.12770032417, 3291461.5860947478], [409713.1167003244, 3291178.564894742], [409452.3760003654, 3290843.2103947336], [408657.6734003761, 3287843.040094671], [408642.905400365, 3287732.9872946674], [408375.6570003645, 3285705.8360946225], [408460.09740039357, 3284170.868494596], [410089.69130034343, 3282730.8714945684], [405227.3327003777, 3272504.0676943506], [405186.44650039036, 3272418.079294343], [404836.3757004041, 3271681.886894335], [404808.2497003433, 3271639.2485943283], [404765.1433004044, 3271559.828494327], [404696.4225003483, 3271413.4447943247], [404555.2617003913, 3271110.5449943226], [404480.08690036833, 3270949.065194318], [404296.334600381, 3270595.079494308], [404151.73110041337, 3270316.512894302], [404152.6193003721, 3270293.366394297], [404208.78920035413, 3268829.614194272], [404195.0166004043, 3267690.337994246], [404190.8502003662, 3267488.915094239], [404183.7629003658, 3266796.4612942287], [404178.414000425, 3266564.8155942196], [404178.1009004098, 3266354.793994215], [404175.9011003916, 3266020.808094215], [404175.71440037683, 3266010.0161942123], [404175.400000378, 3265991.91829421], [404175.06920034665, 3265972.8759942125], [404164.4419003434, 3265361.110194201], [404156.46930038056, 3264941.370794184], [404158.03830038826, 3264528.4764941777], [404147.3779004231, 3263710.790194164], [404137.5875003512, 3263160.32069415], [404134.44270038407, 3262980.7995941495], [404134.74730041716, 3262824.4054941423], [404124.85270034696, 3262378.106794132], [404108.63910037524, 3261010.781994106], [404103.0034003947, 3259884.2165940814], [404087.2081003641, 3259332.6538940687], [404057.9952003663, 3257259.4967940315], [404061.72110038373, 3257167.8562940233], [404013.72440036054, 3253943.652593956], [403884.4922003784, 3253945.303393958], [398393.6359003861, 3254015.2295939564], [396994.22220041987, 3254033.130793959], [396994.00240044366, 3254016.3789939587], [396992.015900449, 3253865.013193953], [396966.3257004253, 3251907.8532939134], [396947.42980044073, 3250468.1509938804], [396418.8883004481, 3249243.429293853], [396963.8063003943, 3247534.859893824], [397752.11890041997, 3247589.8489938234], [398012.12880040513, 3247087.6798938145], [397905.99270042556, 3246628.2894938057], [397337.5563004466, 3244764.71939376], [398389.8605004138, 3243581.533793737], [398400.9516003911, 3243475.7932937387], [398670.2984004218, 3240908.2907936764], [399181.43640043575, 3239137.2699936396], [398868.29620035616, 3237414.316193601], [398867.4066003535, 3235963.109393579], [398744.7736003536, 3235105.555093553], [398706.45000035455, 3234431.7622935455], [398783.09540041984, 3234048.926293536], [398746.02950036625, 3233957.958193533], [398623.3813003755, 3233761.9215935324], [398582.3848003883, 3232459.177493502], [398596.04610041325, 3232439.8309935057], [398600.62890038197, 3232406.0586935026], [398587.24260043015, 3232383.5073935], [398590.50710035773, 3232377.2883934965], [398596.1450004247, 3232373.529393502], [398606.5038003986, 3232375.905093503], [398614.0058003574, 3232375.807393501], [398620.19420040934, 3232367.6895935037], [398641.99230041716, 3232341.429193495], [398667.56550042256, 3232332.2781934966], [398682.3214004114, 3232317.0621934975], [398683.26080042403, 3232302.2070934996], [398673.8250003782, 3232283.6741934987], [398650.67040037597, 3232274.454093493], [398638.05240036, 3232266.2906935005], [398638.1056003562, 3232240.770993494], [398647.2273003829, 3232208.6093934937], [398786.41440035315, 3232010.871793491], [398826.9964004371, 3231968.0171934906], [398899.5909003805, 3231958.93649349], [398948.24990038155, 3231912.2142934916], [398984.4497003582, 3231877.5283934884], [399004.0924003715, 3231820.966093491], [399101.2061003563, 3231790.7635934902], [399142.89950037363, 3231776.7549934816], [399169.75240042806, 3231766.1266934914], [399135.16940038383, 3231639.69099348], [399173.72660043027, 3231584.688293485], [399239.475800433, 3231536.4279934852], [399365.9992004172, 3231490.3170934776], [399453.97740041645, 3231426.1831934834], [399501.92280035466, 3231317.5608934727], [399644.2043004066, 3231226.651293477], [399785.4980003632, 3231200.480293479], [399859.4812004033, 3231159.916093474], [399911.08340039494, 3231114.930093469], [399983.93940037146, 3231088.1860934747], [400024.30560039973, 3231088.4241934763], [400080.47490036336, 3231112.5848934758], [400113.86720042705, 3231119.9308934757], [400144.4667004261, 3231117.543293477], [400166.4715004221, 3231105.788593473], [400188.3271004073, 3231095.2153934767], [400152.7340004146, 3231055.791593474], [400100.6527004288, 3231020.174393476], [400021.1028004203, 3230975.618293474], [399975.7294003614, 3230954.6721934746], [399938.29920038243, 3230965.9052934665], [399904.5156004131, 3230990.39309347], [399835.46870041464, 3231000.888793466], [399800.32250041544, 3230980.9850934735], [399728.4847004226, 3230903.325493474], [399664.4686004045, 3230772.4418934626], [399597.09000038024, 3230738.7321934644], [399572.6438003788, 3230689.9302934636], [399526.34510035964, 3230663.498793467], [399445.5414003893, 3230611.594193461], [399394.8826004374, 3230544.693993464], [399256.0826003557, 3230418.4354934557], [399154.42820037453, 3230119.98739345], [399164.09320039063, 3230033.1276934533], [399135.57680042664, 3229938.4583934466], [399086.38410038187, 3229795.160993449], [399060.88430041086, 3229707.4862934463], [399067.26160040376, 3229648.1494934377], [399057.92020041496, 3229626.8218934434], [399045.64390043344, 3229611.717993443], [399028.4898004174, 3229611.755493443], [399015.31700035476, 3229619.5434934413], [398995.299200424, 3229630.445093443], [398984.5290003643, 3229651.293393443], [398980.75910041475, 3229667.444493443], [398970.35680043057, 3229669.3160934397], [398958.51220043655, 3229656.3139934405], [398953.48110043025, 3229644.4228934473], [398938.3061003923, 3229596.042093436], [398943.30100039387, 3229563.0643934426], [398952.906900357, 3229539.314193436], [398995.99270039937, 3229447.51679344], [399015.4578004279, 3229279.1607934367], [399004.25820035156, 3229237.5264934297], [399007.2404003667, 3229196.1647934336], [399032.17520042, 3229167.9584934283], [399040.3293004164, 3229145.897893429], [399042.43050039, 3229121.5702934344], [399028.80170039466, 3229096.755693429], [398990.9905003895, 3229057.4887934313], [398929.3550003751, 3229013.933893428], [398872.13760037627, 3228954.886193428], [398804.2392004088, 3228789.4355934192], [398746.4118003916, 3228729.4596934197], [398685.2402004291, 3228684.1309934254], [398588.6267004304, 3228679.385593419], [398477.4123003813, 3228633.3188934177], [398450.4474003941, 3228605.3233934245], [398432.2394004354, 3228568.91149342], [398413.78020035336, 3228468.070693419], [398408.63570043317, 3228439.1710934127], [398419.8871003612, 3228418.622693418], [398444.0954003617, 3228406.664693417], [398449.3842004357, 3228386.9172934163], [398471.74050043954, 3228311.8699934096], [398439.2180003672, 3228231.889493412], [398430.44660039374, 3228215.844293411], [398453.42340037535, 3228160.4706934122], [398477.0411003734, 3228119.8440934108], [398490.04400042107, 3228060.490293406], [398506.68030038784, 3228005.6141934036], [398518.1881003662, 3227959.540193404], [398478.8265004003, 3227877.8196934], [398480.81770043395, 3227815.9141934062], [398475.682800417, 3227793.578893403], [398513.999500396, 3227649.2916934], [398542.8331003854, 3227536.0166933998], [398546.73450035544, 3227511.3162933905], [398561.7927003562, 3227483.0926933964], [398559.26770041324, 3227403.6057933974], [398548.1115004191, 3227361.4154933956], [398535.5970003846, 3227327.4969933955], [398531.8456004282, 3227288.6815933893], [398590.3217004232, 3227219.8200933933], [398626.829500383, 3227177.4505933863], [398691.7428004215, 3227138.7211933914], [398786.03040038265, 3227106.594593385], [398841.7770004141, 3227062.3633933896], [398879.3104003707, 3227043.514593387], [398896.66820039094, 3227019.549693386], [398898.47470040235, 3226995.959393381], [398919.05140041525, 3226967.5589933875], [398916.16600038216, 3226947.674893382], [398913.5239003628, 3226920.9957933803], [398925.9385004319, 3226847.341893385], [398927.23380038375, 3226815.9771933826], [398911.7595004205, 3226737.190093381], [398926.77830038953, 3226702.6233933754], [398946.5813004131, 3226678.490693381], [398976.41910039796, 3226673.867593376], [399002.52600038785, 3226669.9158933777], [399026.60330038634, 3226655.5225933837], [399021.04380040505, 3226635.358293375], [399028.07150035014, 3226613.8352933773], [399059.24920038425, 3226582.6099933772], [399109.59310042975, 3226533.469193376], [399133.1003003704, 3226463.8842933737], [399163.77080037305, 3226427.3404933717], [399186.2987004068, 3226361.895493374], [399187.1651003963, 3226268.880893371], [399166.3688003755, 3226209.5237933653], [399127.4113003634, 3226131.899793365], [399089.7972004177, 3226074.3322933675], [399027.88960035576, 3225992.747993362], [399009.9655003923, 3225882.522793365], [399022.19980037975, 3225819.5043933634], [399034.27530036395, 3225772.195093361], [399050.9828003886, 3225731.062593358], [399089.6080003691, 3225688.352693362], [399150.2267003547, 3225639.5237933565], [399150.0555003775, 3225629.260693356], [399140.8640003522, 3225610.567893354], [399131.4251003915, 3225600.6647933535], [399114.6009003613, 3225583.197393356], [399091.25390042935, 3225553.313393358], [399073.8953004305, 3225523.4795933524], [399073.12790043524, 3225499.9975933502], [399080.4633004044, 3225483.1591933537], [399097.48350039124, 3225452.7982933572], [399109.1186003866, 3225428.3612933494], [399094.0562004283, 3225391.4473933536], [399099.2081003702, 3225325.665993351], [399123.09870037914, 3225263.495793348], [398932.9100004336, 3225357.500093348], [398895.5974004321, 3225357.1836933456], [398857.7171003569, 3225342.719693352], [398802.7422003751, 3225301.2457933486], [398642.88550035935, 3225290.5637933523], [398472.83890041296, 3225306.1860933504], [398396.8694003597, 3225284.041093347], [398310.0142004151, 3225268.624193345], [398273.80370035453, 3225276.445993354], [398182.4465004181, 3225314.802193346], [398098.9924003785, 3225351.6457933537], [398026.77600037144, 3225363.7495933534], [397890.10440037, 3225359.9934933465], [397786.2569003885, 3225362.508993348], [397737.33680041303, 3225321.517693351], [397681.20410035783, 3225265.2847933457], [397660.59140036453, 3225250.344293346], [397631.77430042333, 3225241.8900933443], [397578.68730042095, 3225234.1042933473], [397560.799100418, 3225235.458993347], [397548.1256004374, 3225241.3612933466], [397531.1180004263, 3225258.501293349], [397501.9294004092, 3225265.5855933535], [397479.89570040215, 3225261.870193349], [397447.1780003799, 3225246.2917933483], [397377.74030040053, 3225201.442493343], [397291.0233003579, 3225171.573293348], [397266.32310040103, 3225142.9516933486], [397228.14200036495, 3225118.403893342], [397202.05180042074, 3225082.2406933466], [397180.69030036905, 3225040.0567933465], [397140.92330035625, 3224999.41679334], [397095.13770043815, 3224975.115093343], [397091.9120003568, 3224946.242993344], [397098.0986004229, 3224909.0284933397], [397110.79780036176, 3224893.42259334], [397125.8145004319, 3224886.28309334], [397136.9806003686, 3224872.7200933374], [397135.0979004301, 3224852.33859334], [397119.8229004431, 3224831.0867933356], [397101.2076004105, 3224810.1798933377], [397096.06530038995, 3224786.5830933414], [397101.86240038864, 3224753.0798933376], [397111.94880036544, 3224733.8971933424], [397101.8495004162, 3224689.783693336], [397072.87130041653, 3224633.689393339], [397050.6061004199, 3224595.6337933303], [397033.2270004244, 3224569.793493333], [397018.32610037376, 3224556.870493337], [396987.8847003999, 3224559.0815933365], [396972.1148004042, 3224549.2703933367], [396961.7667004091, 3224535.7202933286], [396951.0090004401, 3224509.6375933257], [396934.19180036645, 3224473.42479333], [396924.20960038743, 3224461.5124933287], [396919.29740038957, 3224455.9529933357], [396912.0253003775, 3224453.8654933283], [396898.70030037116, 3224453.932293329], [396892.43400036567, 3224451.506493337], [396888.9692004209, 3224436.2167933304], [396887.06800038106, 3224419.659593327], [396884.6905004078, 3224404.98949333], [396867.6754004161, 3224390.035693323], [396847.36230042117, 3224388.660893327], [396781.4758004255, 3224403.7813933324], [396740.5382004045, 3224420.5355933253], [396672.1423004462, 3224435.577593328], [396598.3907004355, 3224433.7737933267], [396514.3349003717, 3224413.2199933357], [396482.09240040067, 3224412.3070933255], [396464.46120044583, 3224423.939093328], [396436.3615004269, 3224430.806693328], [396396.10280044604, 3224430.9461933314], [396340.667800384, 3224425.22949333], [396305.5657003624, 3224414.2633933304], [396258.76950036024, 3224399.152793328], [396215.6581003728, 3224396.3611933286], [396171.90790038987, 3224375.7068933314], [396122.5306003866, 3224350.093993327], [396067.0210003831, 3224309.5661933315], [396044.8388003711, 3224307.6589933257], [396016.58000036416, 3224313.523893328], [395998.1398004067, 3224321.9393933285], [395976.8910003797, 3224348.7641933323], [395960.15150043915, 3224361.1601933306], [395934.74910043704, 3224364.886293332], [395908.69740039756, 3224365.789193334], [395875.4954003929, 3224369.567493328], [395844.482500397, 3224386.199093332], [395821.2092004074, 3224402.598593325], [395806.9693003713, 3224424.3179933326], [395797.23090041813, 3224435.694193327], [395787.601500403, 3224439.3721933262], [395773.2370004106, 3224441.300393328], [395745.08140042063, 3224439.977793329], [395712.30100037873, 3224444.6292933295], [395674.1400004035, 3224453.976393334], [395649.1952004211, 3224476.0660933284], [395622.69760043337, 3224503.88709333], [395568.7758003843, 3224536.727793333], [395538.8909003756, 3224556.9402933344], [395521.51860037114, 3224558.85649333], [395467.84060037474, 3224547.8442933364], [395437.10430044413, 3224519.0532933325], [395428.92590044596, 3224487.010993333], [395427.70060039696, 3224475.8875933285], [395402.1316004328, 3224476.6853933325], [395371.1771004011, 3224480.762593334], [395340.2586004343, 3224481.872093331], [395297.5511004498, 3224494.5198933305], [395285.66660043586, 3224522.616793333], [395228.24180036585, 3224621.329893332], [395166.54580045084, 3224659.4596933313], [395110.1743004053, 3224690.2550933408], [395017.3989003678, 3224732.255493339], [394809.3843004181, 3224952.1809933437], [394753.7788003946, 3224986.0496933404], [394710.7369004395, 3225008.7159933387], [394674.3083004006, 3225020.1936933445], [394643.7375004494, 3225015.1748933382], [394625.37820042705, 3225006.7104933388], [394615.1840003851, 3225000.8459933437], [394603.1204003977, 3225001.7692933446], [394531.4191004045, 3225052.7140933415], [394462.7587004446, 3225090.2938933433], [394411.20050041634, 3225101.597293347], [394362.3181003762, 3225122.6643933426], [394329.6105004557, 3225134.417993349], [394296.9631003855, 3225154.785893351], [394199.2105004279, 3225201.6928933463], [394122.4992004212, 3225208.974993351], [394046.3351003686, 3225255.593893345], [393988.9892003884, 3225269.738693344], [393936.4657003886, 3225280.2586933477], [393890.9662004158, 3225277.9513933486], [393841.7445004168, 3225271.293793347], [393816.3201003939, 3225262.857393347], [393784.5594003977, 3225245.10849335], [393740.0402004168, 3225277.9793933462], [393665.77410037693, 3225352.9748933525], [393641.3353004168, 3225406.885993353], [393617.802100428, 3225438.2003933503], [393524.8250004198, 3225492.86929335], [393403.6854003766, 3225579.286993354], [393312.877100413, 3225643.5959933554], [393279.27600038855, 3225659.307193356], [393079.7863003819, 3225801.643293359], [393002.4858004212, 3225821.4771933584], [392905.87750041555, 3225843.8418933633], [392764.6914004011, 3225869.814593359], [392704.89550043445, 3225885.811893358], [392577.2263003754, 3225914.7217933577], [392474.3561004173, 3225928.6838933597], [392447.2531004398, 3225923.4455933617], [392382.73390041804, 3225892.3506933656], [392187.36220043426, 3225882.676093364], [392039.73550038505, 3225887.9440933596], [391950.4866004166, 3225904.6080933623], [391835.4437004528, 3225954.5959933563], [391588.3442004346, 3225977.18179336], [391526.023300398, 3225999.0382933663], [391488.59640043887, 3226016.8399933632], [391444.6828003933, 3226004.531893363], [391400.142200447, 3225989.7055933652], [391325.88770042814, 3225989.2528933664], [391230.9879004591, 3225901.5096933604], [391069.74950040574, 3225792.225693357], [390995.96990046144, 3225738.87309336], [390954.8675003832, 3225718.469293361], [390903.3239003982, 3225714.0084933504], [390854.91330044664, 3225636.552893354], [390833.0463004339, 3225628.701893357], [390760.3146003972, 3225501.064493354], [390720.20000039646, 3225412.3299933523], [390728.6122003988, 3225048.16029334], [390685.2878004403, 3224602.384393331], [390676.6230004284, 3224373.0042933277], [390663.6264004377, 3224191.2330933223], [390628.96690039994, 3223944.5406933166], [390624.8365003979, 3223687.131093312], [390646.4991004584, 3223410.1422933065], [390662.7083004229, 3223209.7147933054], [390663.40330045833, 3223063.2660932965], [381000.28650050145, 3223184.5621932982], [381001.6222004927, 3222988.448693296], [380997.1725005057, 3221110.088893253], [381715.1833004473, 3221093.5459932536], [381697.48180048226, 3220865.4052932546], [381704.71560050093, 3220384.6673932453], [381705.0868004323, 3219059.2333932095], [381702.2970004276, 3218534.080193199], [381698.60850048566, 3216159.6136931456], [382781.65660043573, 3216148.9691931503], [382727.8794004439, 3215152.174793125], [382724.7631004928, 3214659.8069931217], [384509.41930045735, 3214647.2632931224], [384507.96030045266, 3213859.1736931], [384507.03030046826, 3213513.100093092], [384493.72220042674, 3213136.3531930894], [384497.2032004744, 3213003.0153930853], [384707.84150045883, 3213025.060193086], [384859.1427004357, 3212682.7690930795], [384989.81660045794, 3212398.17919307], [385503.41360046866, 3211256.370593046], [385803.9759004572, 3210579.234793036], [385616.07600043085, 3210522.705693029], [385510.87440045684, 3210484.5792930303], [385268.20910043886, 3210521.855493032], [385043.41450043034, 3210592.6438930347], [384837.96390042163, 3210646.700493031], [384676.70960041555, 3210698.041493032], [384449.51300048665, 3210792.779893033], [384193.2951004816, 3210839.2367930333], [384013.3220004257, 3210892.845893034], [383846.78260041657, 3211001.2867930415], [383700.01360041497, 3211101.8330930434], [383627.27500049013, 3211141.349093042], [383593.64350045985, 3211196.7195930425], [383563.3305004461, 3211265.248193042], [383465.08100042946, 3211386.6474930476], [383385.96110043576, 3211406.1365930536], [383308.0022004518, 3211437.4118930507], [383264.18060046626, 3211461.4196930467], [383176.325000428, 3211531.4202930513], [382980.49600046285, 3211517.6614930523], [382900.9201004827, 3211517.949893053], [382810.66390043485, 3211535.4696930484], [382713.8838004331, 3211559.034393055], [382571.51690049144, 3211587.4791930555], [382392.912000436, 3211626.265493054], [382508.5019004346, 3211428.260193051], [382662.4297004343, 3211172.3522930397], [382856.9315004584, 3210938.5558930426], [383117.28890041274, 3210650.3998930324], [383160.1791004869, 3210602.5047930325], [383318.2476004151, 3210487.0087930337], [383421.46590041084, 3210334.0101930266], [383455.72320041916, 3210244.079493026], [382354.0489004369, 3210235.0537930243], [382341.71790048364, 3210234.9515930256], [382915.9183004298, 3208668.4413929875], [382977.57910044503, 3208500.2262929855], [383358.7560004642, 3207796.8410929698], [384592.5307004244, 3204890.1222929107], [384638.3534004126, 3204790.595292905], [384739.90510044544, 3204568.117592901], [385475.40240044956, 3202803.8421928636], [385619.3643004087, 3202458.527092856], [385768.03700046893, 3202145.9486928517], [386260.4232003951, 3201000.784592826], [386234.82170047396, 3200949.4266928295], [386249.0697004516, 3200881.5404928294], [386265.4307004386, 3200853.252592825], [386301.0857004786, 3200825.520392821], [386335.1938004389, 3200807.984092826], [386391.7405004344, 3200816.916392822], [386421.6679004485, 3200856.4824928283], [386540.2898004469, 3200916.1844928255], [386665.9395004327, 3200895.0291928304], [386807.3615004549, 3200843.635892822], [386901.6466004113, 3200787.9633928235], [386983.5473004665, 3200740.185292825], [387017.9869004619, 3200730.5187928225], [387054.74640047003, 3200734.4485928225], [387122.5648004088, 3200739.170692822], [387217.577700477, 3200724.042492821], [387290.5084004019, 3200715.996492823], [387375.2509004587, 3200697.8005928197], [387507.29760041914, 3200674.3947928236], [387623.3977004672, 3200656.2563928184], [387700.0278004471, 3200648.2402928215], [387799.05200039555, 3200612.885492816], [387892.8100004031, 3200588.822492818], [388045.2170004552, 3200563.703692819], [388183.02700040594, 3200535.277692815], [388249.63300041104, 3200526.8204928157], [388302.31820039183, 3200525.534792819], [388441.2244004024, 3200443.187792819], [388522.27750039194, 3200387.437492817], [388608.6536003967, 3200323.4373928173], [388682.2121004041, 3200279.5109928097], [388755.51310038776, 3200228.6076928102], [388852.36370039784, 3200176.934992814], [388909.5144004359, 3200136.1290928074], [388985.93090041354, 3200091.993392807], [389055.3685004638, 3200062.270992805], [389081.4940004455, 3200042.0727928085], [389101.88270044327, 3200011.863492805], [389134.6039004368, 3199981.041592809], [389179.5716004432, 3199973.7937928075], [389240.63960038446, 3199971.5977928075], [389332.5599004316, 3199931.897792809], [389466.986600426, 3199855.8387928046], [389507.6918004012, 3199836.1047928045], [389605.583800447, 3199834.5600928026], [389724.4418004218, 3199823.7670928077], [389818.1306004053, 3199807.5685927994], [389887.43610038905, 3199802.876092798], [389950.95960039034, 3199797.0623928015], [390007.53630043525, 3199783.8530928046], [390066.8710004017, 3199778.802392799], [390106.74710041535, 3199786.445592805], [390183.09420039173, 3199812.7517928025], [390221.45700043865, 3199826.1397928004], [390247.1155004569, 3199833.173992802], [390292.1948004582, 3199845.9997928026], [390340.4815004055, 3199856.953592799], [390411.95410041424, 3199841.999192798], [390482.0368004208, 3199828.082392803], [390465.450800385, 3199816.1910928064], [390435.4534003851, 3199792.358692804], [390365.076200449, 3199701.0364928013], [390328.50790045806, 3199610.1214928], [390320.90800040314, 3199505.2905928004], [390313.7755004555, 3199424.5290927934], [390264.43770042085, 3199326.3178927884], [390232.446300429, 3199265.6012927922], [390197.94790042634, 3199198.000692786], [390180.6187003782, 3199144.4826927874], [390152.31310040754, 3199088.9206927875], [390127.32610042085, 3199046.684192789], [390128.9323003792, 3199010.9555927855], [390138.7806004474, 3198976.3008927843], [390152.1216004389, 3198950.8833927857], [390202.63820043637, 3198910.1763927815], [390230.7341003791, 3198881.375392784], [390291.1229004304, 3198844.0254927855], [390330.38860038656, 3198807.1890927814], [390369.6897004442, 3198768.5173927783], [390387.579000436, 3198690.607792782], [390391.8709004624, 3198641.6748927734], [390394.82220042427, 3198603.3372927792], [390394.821700426, 3198529.5943927728], [390397.7742004126, 3198479.45759278], [390397.7746004502, 3198417.5228927727], [390397.77480038686, 3198355.5792927733], [390394.822900449, 3198302.491092773], [390400.79840040347, 3198235.2095927685], [390399.4926004128, 3198184.509092772], [390394.8220004544, 3198137.3178927707], [390400.72590040934, 3198098.978792768], [390400.40760042914, 3198046.296592767], [390367.99370039254, 3198031.640192767], [390340.26220038807, 3197999.5397927635], [390315.58840045385, 3197971.644492766], [390308.4395003952, 3197926.39059276], [390306.06030038896, 3197888.2851927606], [390310.8309004171, 3197851.8616927606], [390326.79110044206, 3197813.0214927634], [390329.6921003828, 3197783.8627927625], [390342.6364004435, 3197749.638892758], [390354.4206004441, 3197714.8076927625], [390403.4159004048, 3197644.632692753], [390431.5866004288, 3197602.5586927533], [390444.4283004443, 3197553.851792757], [390457.3795003822, 3197506.400492756], [390500.54260044475, 3197430.9134927457], [390541.5529004532, 3197361.889692745], [390575.0412004463, 3197303.1296927505], [390607.1519004076, 3197234.765592743], [390633.683100392, 3197171.9760927465], [390672.7724003777, 3197113.379592744], [390722.38290039264, 3197060.344992747], [390768.9666004031, 3197015.7198927444], [390799.0111004127, 3196950.5793927396], [390848.47060043074, 3196893.086792743], [390869.7625004109, 3196870.5783927394], [390882.73460041493, 3196846.86869274], [390899.9581004149, 3196819.073192737], [390918.4794004449, 3196787.0169927333], [390980.645700383, 3196762.9065927356], [391012.68040046346, 3196682.34649274], [391047.9600004314, 3196614.402592732], [391079.67880046205, 3196550.523892732], [391124.85500037746, 3196465.844492735], [391168.30480046186, 3196409.9778927322], [391265.6972004421, 3196301.7713927296], [391329.9105004573, 3196229.7977927253], [391367.35590044013, 3196165.836192721], [391405.8175004189, 3196091.2394927265], [391418.88900041836, 3196070.625692727], [391415.0572003936, 3196028.0316927196], [391433.16540037614, 3195985.8633927214], [391469.2924003985, 3195993.5667927247], [391513.93380038836, 3196013.510492717], [391543.05960043025, 3196048.168092723], [391589.3688004175, 3196051.3029927216], [391643.3084004603, 3196059.969292719], [392957.75310042367, 3192633.293892647], [392276.9298004534, 3192195.89969264], [392553.6419004176, 3191839.9283926305], [393239.89530039387, 3189883.7583925887], [394136.0751004242, 3188234.6389925573], [393734.18190042255, 3186086.6502925116], [398670.27890036395, 3183056.889992447], [400673.2999004162, 3181827.4385924144], [400735.4769004194, 3181789.2747924156], [400757.0175003709, 3181776.055792414], [400766.3402004036, 3181770.332792411], [400942.59470033395, 3181662.146592416], [401673.2331003955, 3181213.683892409], [402101.24720040854, 3180950.9703924], [402851.1663003953, 3180490.6717923917], [402851.1956003969, 3180490.6537923906], [402966.5906003864, 3180419.8256923878], [402977.00330032787, 3180413.432992389], [403016.9236003794, 3180388.931492386], [403057.2375003739, 3180364.186392387], [403097.42530034704, 3180339.5200923863], [403137.52770037414, 3180314.9043923854], [403178.20250037545, 3180289.9383923886], [403217.8642003324, 3180265.5948923873], [403258.3401003769, 3180240.748392384], [403267.3805003491, 3180235.2005923823], [403300.1532003436, 3180215.0863923794], [403396.8902003913, 3180155.7083923854], [403464.1309004007, 3180114.435192385], [403593.4441003747, 3180035.0632923823], [403690.11210039724, 3179975.7281923746], [403754.0883003641, 3179936.459592377], [403786.5023004022, 3179916.5647923755], [403818.9162003725, 3179896.6700923727], [403843.45720036706, 3179881.6068923743], [403843.6238003959, 3179881.5046923743], [403854.5409003339, 3179874.8037923756], [403866.937300388, 3179867.1948923725], [403887.11980038136, 3179854.805492378], [404088.399000358, 3179731.263592373], [404383.10200036864, 3179550.373292372], [404908.3370003509, 3179227.9878923646], [404922.98760039866, 3179218.9950923626], [405219.2154003247, 3179037.169392358], [405239.4502003724, 3179024.751892361], [405370.48940034315, 3178944.318592361], [405622.69100036344, 3178789.518592358], [405831.14200034784, 3178661.5724923545], [405845.85050039156, 3178652.544892349], [405847.6103003505, 3178651.464692355], [405853.31410037604, 3178647.9634923516], [405886.31110036705, 3178627.7092923475], [405894.81820039306, 3178622.487592348], [405898.9040003815, 3178619.979692346], [406275.1201003539, 3178587.76739235], [406671.47030036, 3178553.8289923454], [406676.96900031395, 3178553.3582923533], [407075.32080033165, 3178519.2504923437], [407327.0999003674, 3178497.690792346], [407536.52980034397, 3178479.7592923413], [408535.301100344, 3178394.2398923473], [408712.6838003304, 3178379.0512923473], [409235.86310031416, 3178314.260392341], [409649.60940032674, 3178292.9994923435], [411015.85700034327, 3178222.795992341], [411359.3737003382, 3178205.144792345], [411482.44040036027, 3178198.8200923386], [411603.4539003393, 3178190.010292343], [411735.70170036476, 3178180.3786923406], [412069.36610034324, 3178156.0886923387], [412124.7257003101, 3177863.6311923335], [412160.0818003175, 3177676.8492923332], [412090.49140029616, 3177376.1697923257], [411979.44600033836, 3176896.3480923087], [411866.1141003696, 3176406.6690923], [411752.67100036575, 3175916.5101922876], [411636.7728003139, 3175415.7406922835], [411574.2603003658, 3175145.6414922737], [411517.15500030736, 3174898.9002922713], [411514.56510036805, 3174887.7003922695], [411286.10220031155, 3174260.0188922584], [411009.8678003346, 3173501.0996922404], [410804.1493003257, 3172935.9088922297], [410623.11610033584, 3172438.5404922185], [410557.42680036486, 3171974.2700922014], [410445.74650037603, 3171184.980492193], [410362.7645003535, 3170596.9807921806], [410132.0214003392, 3170650.119692175], [409915.51650031, 3170699.9799921843], [409698.5090003742, 3170749.9601921765], [409480.39000032196, 3170800.1890921853], [409262.61330038554, 3170850.3496921803], [409045.0490003057, 3170900.4484921796], [408827.47560032795, 3170950.56149218], [408687.9266003477, 3170982.6998921833], [409146.4481003536, 3172838.011192226], [409297.2430003716, 3173164.0865922347], [408419.3323003224, 3171673.696192196], [408435.11400034075, 3171670.163092201], [408268.1111003663, 3171381.2140921927], [408185.44660032244, 3171246.2604921903], [408109.5695003331, 3171113.431192182], [408092.7541003146, 3171083.9475921877], [407926.03360036074, 3170813.82159218], [407769.0512003168, 3170541.443692174], [407749.4165003138, 3170509.3666921714], [407738.76300034096, 3170491.9621921717], [407690.7102003873, 3170407.0524921697], [407690.4427003401, 3170406.5797921703], [407642.41740035405, 3170332.2776921703], [407632.2408003203, 3170337.512592174], [407082.47270030517, 3169404.229292149], [405882.58440032974, 3169079.0513921455], [406240.77930035547, 3167792.6449921145], [406506.5306003118, 3167414.53399211], [406503.52480035234, 3167397.3113921094], [406502.4924003509, 3167391.3960921033], [406499.76030032, 3167375.7407921096], [406497.06890036527, 3167360.319592103], [406496.2271003929, 3167359.0831921073], [406488.9395003392, 3167353.505992103], [406479.1872003336, 3167353.880992102], [406470.20780038356, 3167348.710892102], [406450.88590032014, 3167178.832892103], [406463.0684003186, 3167168.1536921067], [406461.9158003772, 3167158.9023921047], [406461.9140003309, 3167158.888992104], [406461.91230037453, 3167158.8779920996], [406461.9117003947, 3167158.8735920982], [406416.0373003695, 3166896.0377920945], [406258.45910033345, 3165993.156992074], [407450.35180035, 3165744.422692074], [407763.51650031906, 3164632.195892048], [407763.5248003253, 3164632.16659205], [407772.4317003306, 3164600.5336920507], [407798.4166003733, 3164508.2478920417], [407798.8802003153, 3164506.601392044], [407799.3901003851, 3164504.7904920485], [407830.25540037017, 3164395.171892045], [407830.36050033104, 3164394.798692038], [407831.17580038897, 3164391.903192041], [407832.0191003582, 3164388.90779204], [407846.5307003053, 3164337.3700920423], [407851.65070036455, 3164319.1867920374], [408201.53780032566, 3163076.582492013], [408205.0065003811, 3163064.2633920116], [408215.6672003474, 3163026.4031920135], [408217.4024003519, 3163020.24089201], [408217.4298003362, 3163020.143592013], [408232.66510036803, 3162966.0369920162], [408312.47680033254, 3162682.596292007], [408315.89680030773, 3162670.450492008], [408362.98690033704, 3162503.2173920027], [408369.00310030655, 3162481.851592002], [408376.91360037576, 3162453.7586919996], [408379.5130003204, 3162444.5272919983], [408380.02440032834, 3162442.7116919975], [408385.24130031385, 3162424.1842920003], [408374.5346003317, 3162430.189592], [408123.68120031466, 3162570.8879919997], [407881.3776003792, 3162706.7921920046], [407886.8085003123, 3162667.700892007], [407890.9762003209, 3162637.702192008], [408000.1084003058, 3161852.1886919835], [405927.00790035457, 3162406.918291994], [405926.30220037984, 3162407.1071919966], [405923.29040039046, 3162407.913191997], [405883.24830031564, 3162418.6283919956], [405840.70350032445, 3162331.7630920005], [405836.89590038767, 3162323.9888919964], [405815.1264003917, 3162279.5413919967], [405812.4839003673, 3162274.1459919973], [405810.2656003495, 3162269.616691994], [405791.33330031787, 3162230.9619919937], [405788.61810035113, 3162225.418091997], [405786.3690003274, 3162220.826191994], [405762.92360035004, 3162172.9568919926], [405760.75380031636, 3162168.5267919926], [405760.71200038376, 3162168.4414919904], [405758.1689003295, 3162163.2490919977], [405757.6469003558, 3162162.1832919964], [405756.04330039193, 3162158.909091994], [405534.788500388, 3161707.1664919797], [405419.4158003791, 3161471.60779198], [405409.6172003607, 3161451.6016919743], [405402.57400036266, 3161437.2213919805], [405328.501300354, 3161285.9862919776], [405322.8368003445, 3161274.4207919734], [405319.99460034055, 3161268.617691974], [405317.0611003182, 3161262.628391975], [405306.2803003343, 3161240.617291972], [405303.5672003392, 3161235.07779197], [405302.0501003484, 3161231.9803919736], [405237.7995003854, 3161100.7990919743], [405233.90180031746, 3161092.8411919693], [405210.71080036665, 3161045.4919919684], [405208.59920031443, 3161041.180791965], [405205.4578003208, 3161034.7668919703], [405181.762300392, 3160986.3875919683], [405179.3188003933, 3160981.3984919675], [404038.5600004009, 3158652.333991915], [404032.50860039884, 3158573.961191915], [405406.42510034377, 3158931.4230919234], [405788.25160037784, 3159030.7686919235], [405842.49580035394, 3159039.099391928], [405877.79560035456, 3159044.522091924], [405921.8031003111, 3159051.2799919285], [405923.5438003342, 3159051.562991929], [406301.5807003155, 3159112.899191929], [406304.67610032187, 3159113.4017919246], [406307.77140038577, 3159113.905591928], [406453.9437003821, 3159137.627191927], [406787.35300033976, 3159191.736291926], [406805.20010036597, 3159194.6325919284], [406926.546000387, 3158611.113791912], [406959.7664003661, 3158451.414391916], [406992.7143003544, 3158304.5931919143], [407034.2453003882, 3158133.1131919026], [407057.0200003797, 3158065.2853919044], [407121.91470037063, 3157927.2970919046], [407245.40900034, 3157721.6370919016], [407642.15130037774, 3157072.2525918805], [407728.2913003428, 3156929.2115918775], [407983.06070037704, 3156513.0016918695], [408084.69740036497, 3156345.2913918686], [408145.6337003581, 3156244.0661918665], [408190.3515003477, 3156171.386891863], [408222.87920030404, 3156116.081091865], [408248.13370031153, 3156073.1375918626], [408337.30910037993, 3155914.2337918547], [408399.3576003503, 3155806.3667918523], [408412.5904003789, 3155785.7990918537], [408418.150000321, 3155775.9421918537], [408423.4383003582, 3155766.569491856], [408449.8178003627, 3155724.015491856], [408475.3146003445, 3155681.4361918517], [408503.0906003743, 3155640.3560918495], [408597.8543003263, 3155524.399691845], [408690.1332003486, 3155441.3949918495], [408837.6281002991, 3155325.4106918476], [408954.48590030894, 3155233.9904918396], [409146.5975003662, 3155080.4883918385], [409306.10820031393, 3154950.8578918357], [409373.0041003037, 3154903.436091838], [409452.1755003669, 3154861.240591836], [409541.2537003237, 3154816.8430918376], [409794.79900032864, 3154727.720091831], [409983.32480037905, 3154666.965591833], [410027.9000003643, 3154653.1132918317], [410119.9573003593, 3154615.6732918313], [410267.84240032604, 3154537.875891831], [410365.86940032523, 3154481.2453918327], [410453.54400033416, 3154432.296491826], [410915.18180030736, 3154171.049591819], [411424.2231003422, 3153882.5702918163], [411815.26380034647, 3153661.1384918066], [412135.9128003043, 3153480.0999918072], [412172.62090035767, 3153460.079291808], [412250.62980031787, 3153603.2397918063], [412608.97420031676, 3154174.765791819], [412654.2407003178, 3154147.8355918196], [412734.61540030246, 3154000.146391818], [412732.2659003161, 3153964.345491816], [412720.516100356, 3153919.870191813], [412792.46110029344, 3153913.2663918203], [412830.7794002853, 3153891.484191815], [412854.2291002872, 3153809.3470918103], [412876.65040036984, 3153733.6727918154], [412893.84710035124, 3153684.7037918074], [412918.802400335, 3153637.33599181], [412939.0964003345, 3153616.528591807], [412960.3766003367, 3153609.5524918106], [412990.52750031045, 3153610.8481918084], [413012.8511002876, 3153614.171891807], [413048.7755002883, 3153610.594191814], [413128.8799003405, 3153569.4155918085], [413206.37280036334, 3153536.74389181], [413264.85790032026, 3153501.7589918016], [413320.04020030797, 3153447.276291804], [413387.4976003478, 3153399.0796918035], [413473.11440034234, 3153364.237091798], [413574.5923003654, 3153360.689191804], [413638.48460036784, 3153371.7332918043], [413910.05280030513, 3153417.112391801], [414039.76300035196, 3153458.4645918086], [414106.8916003308, 3153525.423191813], [414150.2322003446, 3153590.95159181], [414188.90340028895, 3153638.176291812], [414286.93160028046, 3153643.322891812], [415221.63740035513, 3154369.1428918247], [415332.66440028226, 3154561.0063918317], [415475.40430028655, 3154683.088191829], [415541.8276003272, 3154730.4375918377], [415739.0144002734, 3154481.8349918276], [415916.4728003403, 3154279.533791825], [416221.37610027456, 3154023.0916918223], [416308.31930028694, 3153948.7327918177], [416317.0969003003, 3153880.3026918145], [416262.8108003015, 3153753.4571918095], [416246.22600032156, 3153640.3554918114], [416279.9870003098, 3153550.803491808], [416396.2525003316, 3153476.0370918037], [416411.44970032165, 3153391.0029918044], [416451.4027002973, 3153260.4928918015], [417933.5544002829, 3153643.9004918146], [418094.6215003226, 3153543.532691804], [418245.5324002707, 3153873.6560918186], [418282.0797003, 3153889.648791818], [418313.54040033533, 3153890.269691818], [418347.9277003173, 3153879.2746918174], [418430.8891003454, 3153881.163391811], [418449.9345002866, 3153881.097591817], [418468.4035003227, 3153887.6558918175], [418486.0032002849, 3153905.755091817], [418520.60290032125, 3153944.960391816], [418554.1292002879, 3153951.767791815], [418605.45980029786, 3153919.659191818], [418664.6176003482, 3153909.67669182], [418742.88810030423, 3153918.5635918146], [418812.7864002974, 3153936.9609918203], [418871.89460031415, 3153962.5882918155], [418928.3138003403, 3153962.6429918194], [418976.4324003058, 3153951.550591817], [419018.39700031717, 3153929.3337918143], [419035.9935002963, 3153900.9718918153], [419058.30650027987, 3153849.310591815], [419095.73370028625, 3153766.7509918106], [419133.11140032945, 3153726.799091813], [419158.4372002941, 3153697.5931918155], [419166.5452002678, 3153672.22079181], [419237.5490003432, 3153641.5052918154], [419266.18790032883, 3153623.919191811], [419287.21910027205, 3153608.562491812], [419329.2535002765, 3153588.278691808], [419367.0455002782, 3153586.3905918063], [421949.9217002573, 3155392.45109185], [419853.4323003201, 3152743.607691795], [419629.0640003417, 3152299.8920917814], [418355.3489003432, 3149781.006291728], [418441.1867003058, 3149757.998291726], [418557.34840031166, 3149737.6249917257], [418666.72140031366, 3149721.393691722], [418754.6329003234, 3149709.909591722], [418828.9852002705, 3149698.968391728], [418886.16970028536, 3149689.625091722], [418995.57630030933, 3149663.3763917205], [419117.6970002796, 3149620.7733917264], [419220.5295002685, 3149567.011991721], [419312.5219003403, 3149517.9358917214], [419395.5314002812, 3149475.12879172], [419499.20810028404, 3149420.180891721], [419569.86390028143, 3149383.755991714], [419661.166300324, 3149335.135091718], [419754.3066003352, 3149287.035291712], [419863.8459002717, 3149228.7489917167], [419965.41710029833, 3149177.133491713], [420068.555100288, 3149121.257091717], [420164.6956003382, 3149071.272291707], [420243.6091003224, 3149030.389391706], [420288.3199002559, 3149008.9501917106], [420356.49460028915, 3148973.095491708], [420451.07490033226, 3148921.9592917077], [420546.132000264, 3148871.567391703], [420621.85090031195, 3148832.0724917087], [420686.1321002865, 3148802.205591704], [420749.6323003186, 3148784.132891705], [420795.64640026516, 3148772.060091705], [420844.8595002883, 3148767.715991701], [421039.1809002977, 3148749.899091708], [421670.06300027284, 3148703.5750917057], [422800.19580030476, 3148610.540991703], [422876.2863003157, 3148604.5877916976], [422958.2254002724, 3148600.3318917053], [423013.359700284, 3148596.9574917015], [423056.3778002758, 3148593.3035917], [423188.0190002904, 3148551.1212917017], [423314.390900285, 3148502.6761917016], [423381.0013002509, 3148476.221491696], [423432.8436002764, 3148460.664591701], [423489.2495003119, 3148444.8088916973], [423552.9050002774, 3148426.830291693], [423630.75440030533, 3148409.4100916963], [423727.6648002921, 3148390.248291698], [423807.61550028063, 3148371.4108916945], [423887.0506003003, 3148355.9243916925], [423975.09460028744, 3148337.0180916935], [424074.6395002814, 3148315.208591697], [424164.5165003274, 3148302.597191693], [424262.45080028044, 3148294.3972916915], [425761.78040028916, 3148391.2924916954], [425877.36330028984, 3148402.269291702], [425968.2364002859, 3148412.1782916994], [426046.77940028015, 3148417.366091703], [426143.53690023604, 3148442.458991695], [426242.045000277, 3148476.194691703], [426335.7880002495, 3148491.589291695], [426385.00570031663, 3148491.993691701], [426428.5674002917, 3148485.073891694], [426496.8207002452, 3148463.850691696], [426604.30920025276, 3148431.0833917], [426671.0524002598, 3148409.0894917017], [426759.73580030235, 3148378.939291696], [426819.317000313, 3148361.123291696], [426858.2566003109, 3148348.3019916955], [426921.9953002484, 3148331.8987916936], [426997.0642002912, 3148324.7721916973], [427028.59120026574, 3148323.775691698], [427132.9082002585, 3148331.375691694], [427270.497100267, 3148343.912891692], [427402.77630024974, 3148353.3145916993], [427494.12850028835, 3148361.410991701], [427585.76660028694, 3148376.8618917], [427636.2376002626, 3148391.8562917016], [427670.53000030713, 3148403.573291697], [427708.97550027556, 3148414.932591701], [427758.7538002989, 3148427.8510916964], [427797.5328003123, 3148437.5809916947], [427864.74540027475, 3148450.3165916973], [427927.8823002932, 3148458.4729916938], [428000.58180025, 3148452.998091701], [428056.70130029094, 3148445.4567917], [428340.3663003051, 3147947.848491685], [428361.58640025655, 3147932.938691687], [428423.42930027447, 3147883.4319916843], [428474.0801002919, 3147840.23559169], [428517.6767002459, 3147819.0045916853], [428564.23460026574, 3147779.2204916887], [428610.1273002843, 3147738.7036916804], [428629.31570029154, 3147702.19899168], [428671.8138002831, 3147639.81069168], [428698.01410029107, 3147592.9056916772], [428666.0467002832, 3147435.6979916794], [428653.3036002604, 3147300.754891674], [428616.1108002257, 3147126.72749167], [428597.3621003036, 3146885.280491668], [428639.9333002651, 3146813.134391666], [428712.517100278, 3146725.356891657], [428734.58050026186, 3146649.6725916564], [428704.71450022905, 3146558.4105916563], [428700.13480027625, 3146444.563691651], [428642.74920022755, 3146405.1093916516], [428664.76000027463, 3146337.1795916534], [428727.90770027693, 3146019.3970916495], [428807.2007002726, 3145870.3965916415], [428849.8709002633, 3145789.935991641], [428861.3414002252, 3145759.586491639], [429464.10920028755, 3145855.9301916403], [429752.47630025266, 3145014.0291916234], [430238.0530002235, 3143596.3601915934], [430241.3547002248, 3143586.719691596], [430357.7035002888, 3143247.0331915827], [430398.643300291, 3143127.5068915845], [430420.6697002235, 3143063.199391585], [430642.87490027834, 3140580.413691528], [431116.46930021525, 3135288.739991417], [428771.16920025606, 3135706.828691416], [428159.835400261, 3139001.2405914916], [428083.31620022736, 3139413.5870914985], [428082.5705003051, 3139417.608891503], [428066.69960027834, 3139459.5399914994], [427594.1587002353, 3139093.999391492], [427524.34970024676, 3138208.315791473], [427352.19230025704, 3136024.1110914224], [425832.2286002754, 3136254.073991434], [425802.4252003102, 3136167.990591427], [425826.3706002327, 3136149.5786914243], [425892.2844003065, 3136067.8961914335], [425937.0254002643, 3135980.4448914267], [425958.0524002932, 3135907.995891421], [425974.90250031336, 3135804.8807914197], [425956.5545002761, 3135704.7579914173], [425944.9758002837, 3135636.1737914137], [425899.6503002805, 3135533.40489142], [425861.20550023613, 3135478.1220914153], [425788.39680025657, 3135404.5075914143], [425689.87090024684, 3135342.9028914114], [425617.20600029, 3135313.8262914107], [425540.5921002613, 3135296.9484914117], [425502.77450028737, 3135293.879491412], [425484.22450025636, 3135253.752891415], [425497.7327003004, 3135147.008791404], [425511.7197002951, 3135076.41029141], [425520.1736002929, 3135053.291691404], [425555.87880023464, 3135026.5170914074], [425557.42570028035, 3134946.624091399], [425520.1314002762, 3134772.104791394], [425523.6047002591, 3134682.3083913946], [425522.4056003133, 3134624.6539914], [425447.252900245, 3134566.9268913954], [425384.6063002689, 3134482.276891396], [425367.7588003137, 3134423.721991392], [425363.085400261, 3134373.147991397], [425364.62210028, 3134312.6312913923], [425377.01500024606, 3134268.685591386], [425378.2462002638, 3134201.823691392], [425362.3388003195, 3134119.4084913833], [425343.8888002941, 3134082.741391384], [425380.0804002759, 3134003.952791385], [425376.4101003128, 3133967.0871913843], [425388.8535002905, 3133939.329991379], [425376.0718003205, 3133896.9590913835], [425362.408900319, 3133850.74049138], [425365.87130026816, 3133830.6810913803], [425382.90260029497, 3133805.6979913763], [425387.3706002954, 3133784.498891377], [425379.2369002847, 3133772.05529138], [425366.466400276, 3133768.487391376], [425352.567600295, 3133768.21059138], [425346.8921002834, 3133761.4693913767], [425340.3008003108, 3133737.442891373], [425333.7255002974, 3133686.4144913726], [425350.8028002363, 3133667.4679913805], [425366.0878002355, 3133659.9518913752], [425395.7622003134, 3133663.671391378], [425403.8264003006, 3133651.8423913745], [425408.4263002727, 3133630.5604913747], [425405.10450023704, 3133606.552191379], [425423.4240002901, 3133588.96959137], [425427.0867002398, 3133555.3903913754], [425425.27910029737, 3133494.1025913726], [425432.7360002335, 3133459.7803913723], [425447.83380027895, 3133415.95869137], [425440.08130023617, 3133380.0250913664], [425415.8601003122, 3133354.880991364], [425414.80520031817, 3133320.0175913675], [425474.65570025076, 3133237.7555913636], [425508.55490025773, 3133220.6455913703], [425533.7418002662, 3133205.4384913626], [425573.3687002708, 3133172.7786913607], [425607.5694003158, 3133130.2762913657], [425596.3063002557, 3133037.0617913646], [425597.32290025346, 3132986.665891361], [425645.3384002679, 3132936.7579913544], [425737.7012002702, 3132899.004891357], [425789.99700029776, 3132838.4570913543], [425826.9290002769, 3132770.4575913567], [425860.8728003101, 3132644.9570913524], [425891.83760031307, 3132559.6565913507], [425923.246300248, 3132496.5092913522], [425922.32040029095, 3132453.972791348], [425929.9586002999, 3132426.667391352], [425938.64170027, 3132397.7179913484], [425920.9802002603, 3132362.619391344], [425894.59110023733, 3132329.278291344], [425892.38000025525, 3132321.2675913433], [425884.99040027393, 3132294.472891342], [425892.2643002877, 3132252.3204913423], [425880.08210031304, 3132164.271191344], [425862.53990025, 3132082.67119134], [425852.44790023076, 3132001.9807913434], [425809.4233002981, 3131950.9998913407], [425760.6943002466, 3131875.017591335], [425726.25440027146, 3131790.1657913355], [425685.8712002308, 3131714.5168913347], [425711.48160027276, 3131641.8231913317], [425756.473700246, 3131596.7942913286], [425802.67910029413, 3131557.42139133], [425890.72220025363, 3131490.039591325], [425948.352800307, 3131422.010991328], [425988.7345002788, 3131326.1892913254], [426026.58960024425, 3131250.9890913246], [426049.6494002646, 3131188.5968913226], [426066.5836003066, 3131114.502491316], [426071.5718002641, 3131073.3717913213], [426075.14130029164, 3131016.3779913215], [426074.587700258, 3130972.596291314], [426053.9944002566, 3130933.1950913155], [426000.1329002661, 3130866.658791316], [425943.29210027226, 3130836.730691311], [425899.13080031076, 3130708.1871913127], [425863.2192002831, 3130664.910291309], [425816.1550002778, 3130556.588791307], [425798.8275002876, 3130473.0255913073], [425772.9164002743, 3130424.5146913007], [425749.04230030545, 3130371.690291299], [425726.8631002741, 3130297.0561913014], [425682.5860002709, 3130209.6547912997], [425620.87500028196, 3130153.250091294], [425397.0482003093, 3130022.7451912984], [425338.5461002343, 3129940.299391297], [425328.91200024716, 3129889.795591296], [425333.38760029414, 3129855.2298912914], [425325.7702002417, 3129763.897391292], [425308.2710003156, 3129704.065991288], [425278.6369002291, 3129683.730091288], [425187.28340025316, 3129639.2492912863], [425132.48830024106, 3129609.64879129], [425048.6082003174, 3129578.6192912855], [424987.58850029024, 3129552.6395912883], [424930.0819002883, 3129534.976891284], [424865.9128002986, 3129529.110591288], [424787.9742002549, 3129522.975191285], [424752.09250031563, 3129525.9260912854], [424708.4904003066, 3129558.7485912796], [424674.4243002795, 3129605.574191288], [424618.46790024906, 3129712.6548912884], [424491.1913002739, 3129870.893091293], [424463.1253003181, 3129973.0816912977], [424438.4913002511, 3130005.604891294], [424396.84060028807, 3130019.860991299], [424318.6094002753, 3130028.735991299], [424226.73100023525, 3130057.0981912995], [424187.3152002972, 3130087.693391299], [424096.5154002628, 3130152.082991302], [424000.29590027913, 3130203.486891299], [423874.74330028787, 3130264.5303913048], [423806.767000325, 3130319.111491305], [423825.1467003032, 3130336.985591301], [423798.12730026036, 3130382.0137913013], [423720.4076003168, 3130385.9804912996], [423621.3767002706, 3130410.972291301], [423519.841700307, 3130427.309491301], [423469.1363003193, 3130417.2214913075], [423407.72230024316, 3130385.2231913023], [423267.1312002393, 3130319.5188913043], [423128.8603002798, 3130265.115091303], [423039.3164003097, 3130240.0637912983], [422975.4776003066, 3130226.239791299], [422930.64060030575, 3130215.535291298], [422802.8253002515, 3130195.7601913013], [422602.6908002973, 3130168.8615912967], [422308.3259002833, 3130130.604991296], [422240.90410029027, 3130123.8003912955], [422158.8964003054, 3130113.849091294], [422074.3839003211, 3130102.4013913], [422012.9739003046, 3130094.6699913004], [421937.3108003245, 3130084.1898912997], [421871.09750026284, 3130075.149091295], [421795.2636002475, 3130067.8029913], [421709.06240026787, 3130055.411791291], [421600.2653002893, 3130041.4346912936], [421520.01620025205, 3130032.334791291], [421433.1327002996, 3130021.559891292], [421345.43860029377, 3130009.406091296], [421236.7399003238, 3129993.121591292], [421090.13500029367, 3129974.4611912942], [420967.1390002986, 3129957.630691297], [420833.3175002886, 3129939.07659129], [420739.852400303, 3129927.2993912967], [420611.90270032396, 3129911.7497912906], [420496.64510031056, 3129898.0651912894], [420407.76600032113, 3129886.161091292], [420281.15080033196, 3129869.2821912887], [420130.6261002782, 3129849.090091287], [419944.26400029735, 3129831.5770912925], [419870.62850029283, 3129824.103291286], [419637.70480025705, 3129800.420791293], [419497.2888003309, 3129800.778791286], [419469.29700031294, 3129794.608391293], [419421.18470027804, 3129773.862791286], [419295.1294002682, 3129728.447391284], [419050.25680027367, 3129630.972091288], [418420.25700031454, 3129409.7659912785], [418295.46430032206, 3129372.4200912807], [418113.23810034175, 3129324.914691279], [418671.2193003401, 3128147.0212912555], [418860.9145002974, 3127709.098491249], [418550.4544002728, 3127791.5840912457], [418340.55400027323, 3127796.1481912457], [418150.44050028163, 3127709.6873912406], [417992.3007002736, 3127389.9266912425], [416984.94980034634, 3127547.2390912375], [416937.19500033924, 3127554.6961912387], [416722.4923002893, 3127640.4142912417], [416326.814300335, 3127797.28339125], [415468.93570034154, 3128145.4918912556], [415067.4196003112, 3128193.042891254], [414804.77970028826, 3128227.330091257], [412925.5781002954, 3128360.3571912614], [412666.6995003381, 3128380.7542912588], [412372.4744003418, 3128445.2257912564], [412335.2918003263, 3128439.4467912572], [412278.31730036245, 3128430.591491254], [412267.1751003438, 3128404.560991256], [412164.3301002961, 3128172.963491251], [412063.3385003434, 3128003.735091245], [411191.17820029147, 3126501.767191219], [410732.26380034455, 3125720.3944912003], [410697.4008003599, 3125723.502991202], [410665.20070029335, 3125732.2785911993], [410627.0882003559, 3125762.322291197], [410587.4808003601, 3125800.5684911995], [410542.2655003296, 3125817.763991198], [410499.8686002866, 3125827.3912912034], [410496.04770031304, 3125852.2666912028], [410485.99900029175, 3125872.029291202], [410435.3312003678, 3125890.989391199], [410405.64660031913, 3125898.5433912], [410370.54610032204, 3125901.5660912013], [410316.21920029144, 3125916.6021912033], [410264.3852003133, 3125953.070491204], [410203.8933003118, 3125981.633991202], [410126.3892003179, 3126004.656191205], [410041.7311003074, 3126031.455891202], [409992.9439003397, 3126040.298091201], [409951.34320030536, 3126043.1241912106], [409895.6804003369, 3126061.805391208], [409866.18710030103, 3126058.6567912046], [409823.2795003401, 3126068.9296912025], [409818.9530003124, 3126092.5172912115], [409819.12260034017, 3126114.19939121], [409820.2510003714, 3126139.4129912057], [409812.07890035043, 3126207.145591209], [409791.7676003618, 3126235.3173912093], [409782.45350029186, 3126283.244391208], [409732.3366002986, 3126276.8969912142], [409708.0031002931, 3126236.5205912096], [409535.00890031736, 3125890.887391198], [409514.59000034985, 3125787.025391202], [409481.98290032847, 3125712.830591202], [409458.0982003204, 3125642.551391195], [409432.83770034974, 3125544.853391197], [409411.4264003378, 3125471.8286911966], [409388.8197003226, 3125414.3353911885], [409357.97820035054, 3125330.69669119], [409329.658600311, 3125262.723791192], [409288.2400003191, 3125205.1116911895], [409249.66200030816, 3125186.869591188], [409235.1152003682, 3125144.4725911883], [409255.26990031626, 3125112.9394911886], [409278.1762003464, 3125098.1574911852], [409277.24950031086, 3125048.3871911857], [409243.9186002984, 3124904.062791178], [409213.4532003565, 3124794.6953911763], [409190.51480031013, 3124637.1327911764], [409166.89260035066, 3124451.4227911728], [409156.0008003768, 3124312.599891168], [409080.34140030935, 3124171.879191164], [409020.9483003069, 3124093.7081911666], [408963.532900293, 3124084.579991166], [408935.12310030096, 3124082.537491166], [408926.3342003151, 3124059.5487911613], [408909.8217003607, 3124021.6321911635], [408869.66800033994, 3123950.655591162], [408880.6086003532, 3123881.884091155], [408902.93140030117, 3123855.368291156], [408868.97740036785, 3123750.7548911576], [408773.2514003679, 3123607.104491152], [408646.7636002995, 3123429.7451911457], [408798.49320036895, 3122952.550791134], [408765.9118002943, 3122893.699291136], [408783.3954003388, 3122820.3660911308], [408858.56140032265, 3122497.7771911286], [408276.7002003086, 3121494.772391105], [407939.93070034235, 3120923.1302910955], [407869.7123003617, 3120826.386191091], [407730.87850035966, 3120659.316691088], [407748.61320032383, 3120629.414491089], [407730.3344003478, 3120603.3358910875], [407706.2609003102, 3120574.988991085], [407699.3128003339, 3120564.7002910823], [407701.00380035286, 3120555.3350910847], [407741.32370032626, 3120526.1339910836], [407760.41720035713, 3120498.6675910847], [407741.313400297, 3120452.807591081], [407679.0448003292, 3120391.6209910805], [407618.722300349, 3120336.676991075], [407557.79120029666, 3120286.103391079], [407488.2822002998, 3120281.074091081], [406963.32000035135, 3120237.572291074], [405538.79890038405, 3120098.9726910754], [405270.2339003087, 3120068.8470910727], [404959.3195003496, 3120044.2341910684], [404167.895700364, 3119958.802791074], [404172.5447003138, 3119730.731491067], [404176.48630031815, 3119230.4349910594], [404218.51440036716, 3118346.0862910384], [404222.8868003184, 3118272.520291034], [404225.0337003181, 3118033.335891031], [404236.78380033036, 3117583.9232910215], [404265.670900323, 3116843.4013910023], [404286.1766003296, 3116724.405591003], [404298.7117003495, 3116329.223390989], [404307.8217003675, 3116040.9120909837], [404312.37620031566, 3115816.6342909774], [404325.7039003187, 3115469.888690969], [404372.66410031024, 3113970.4409909355], [404392.8802003468, 3113461.25899093], [404384.53020038636, 3113387.5596909286], [404321.4057003671, 3112903.8197909165], [404304.61040030845, 3112707.410290913], [402306.43750031816, 3113151.548890924], [401374.1410003644, 3113257.9665909205], [399035.6460004043, 3113593.1690909253], [397662.9161004143, 3114158.4343909426], [395127.96110040747, 3113765.7966909283], [390535.01760037686, 3112544.3090909068], [385213.9158004456, 3111702.8665908836], [385054.66670044325, 3111677.6808908875], [384929.04490043386, 3111657.8170908815], [384580.6525003982, 3111602.723890882], [384481.226500436, 3111587.0036908807], [384323.3837004044, 3111562.04209088], [384261.5877004093, 3111552.270290882], [383913.24020046, 3111497.1824908815], [383783.3844004622, 3111476.650490876], [383781.81040039926, 3111476.4020908773], [383703.6292004672, 3111444.6356908744], [383616.39700043545, 3111404.955090882], [383569.87660040095, 3111366.701590879], [383524.23210043815, 3111287.472090875], [383481.09580044245, 3111184.3905908703], [383478.8037004597, 3111155.2678908743], [383470.68510044104, 3111142.0244908677], [383432.6041004197, 3111128.380990875], [383428.24560041504, 3111089.5622908687], [383385.9857004459, 3111058.344790869], [383379.0739004222, 3111049.28229087], [383382.64150039956, 3111040.1173908673], [383389.1650004025, 3111037.471990865], [383389.62830042955, 3111029.476490871], [383386.9334003997, 3111025.424390873], [383373.03380041546, 3111027.000490867], [383365.88810045336, 3111020.254890865], [383366.5603004216, 3110980.071990865], [383355.0056004154, 3110950.575490865], [383337.5534004559, 3110939.660390866], [383322.12180040876, 3110942.591190868], [383315.2746004465, 3110934.932990871], [383318.7344003977, 3110909.198890863], [383315.143900392, 3110886.283890864], [383297.90970039496, 3110866.02289087], [383268.3115003896, 3110848.171890863], [383245.8743003882, 3110832.3926908663], [383244.3522003866, 3110804.3360908623], [383242.44590041524, 3110796.0380908633], [383223.1644004085, 3110785.042390864], [383193.51580043783, 3110777.4345908663], [383179.4540004005, 3110763.3619908597], [383160.10760045244, 3110693.5426908582], [383150.83990043664, 3110656.8031908637], [383143.01130040025, 3110648.6748908637], [383122.248500402, 3110655.5837908634], [383080.99950042757, 3110620.882690857], [383060.51630044956, 3110577.11079086], [383037.1780003996, 3110549.2545908564], [383030.9889004584, 3110493.9889908535], [383026.95070041774, 3110455.9184908587], [383014.4669004646, 3110436.3215908585], [382960.1122004407, 3110400.4837908517], [382875.855100385, 3110385.0276908497], [382853.1452004473, 3110361.6188908564], [382791.75080040825, 3110328.9964908585], [382777.1987004521, 3110284.803390856], [382749.95820040244, 3110254.570590854], [382719.1801003953, 3110234.0621908484], [382698.78730041115, 3110224.9805908515], [382649.3786004153, 3110220.2927908506], [382606.5697004236, 3110218.1771908514], [382517.67910043924, 3110184.6974908486], [382387.99390040635, 3110116.0119908457], [382256.03670042945, 3110254.968390852], [382211.53380046075, 3110309.7120908503], [382181.8889004246, 3110357.3422908555], [382133.1237003908, 3110373.325690854], [382116.1041004265, 3110368.716990853], [382084.94460044696, 3110365.4967908533], [382053.24640043, 3110341.14319086], [382034.1480004648, 3110314.8502908475], [382028.61830047076, 3110298.9683908545], [381957.2358004503, 3110300.4438908543], [381925.8757003938, 3110328.612790854], [381897.7229004131, 3110342.541890857], [381889.208400412, 3110341.3551908513], [381881.95600045734, 3110336.367690854], [381866.32370047196, 3110318.076090854], [381853.5219004685, 3110307.350890857], [381839.32500042923, 3110298.3268908495], [381829.4990004398, 3110286.4221908543], [381821.7498004645, 3110275.8109908565], [381812.72370042204, 3110266.014590853], [381805.4267004387, 3110253.7423908557], [381784.55220046523, 3110237.069490849], [381765.50010044867, 3110220.0074908505], [381740.5860004358, 3110194.8152908483], [381697.5844004114, 3110186.604190852], [381666.61140046094, 3110205.2342908494], [381652.89120047237, 3110229.059590855], [381649.87930046493, 3110265.7548908475], [381666.2975004565, 3110320.2848908505], [381653.41230040137, 3110344.384490858], [381627.9531003993, 3110352.6189908558], [381602.2960004145, 3110347.5271908566], [381565.9259004744, 3110334.1228908557], [381544.5033004126, 3110337.286090853], [381515.28960042814, 3110375.2418908603], [381491.91200039565, 3110421.948390856], [381398.53270040994, 3110442.86639086], [381332.0654003899, 3110423.231090861], [381249.07870042557, 3110497.9299908606], [381214.10270047124, 3110475.0692908554], [381164.4943004522, 3110440.1284908555], [381121.10600040376, 3110417.8924908545], [381061.5876004595, 3110426.757690859], [381009.3140004725, 3110442.8637908525], [380970.95030044916, 3110446.7419908587], [380945.78100040636, 3110429.3942908566], [380925.1700004285, 3110401.994690852], [380913.8296004266, 3110315.2633908563], [380889.3486004451, 3110280.6780908527], [380869.53870041744, 3110272.4735908536], [380836.632900422, 3110285.1141908523], [380809.74140041537, 3110300.902690852], [380789.94160046265, 3110303.5544908578], [380769.1513004759, 3110298.598790854], [380743.21850039816, 3110284.4401908517], [380720.8298004661, 3110283.6254908503], [380699.96570047503, 3110291.1579908547], [380681.7494004325, 3110300.6660908484], [380669.79710043326, 3110311.6663908497], [380659.8919004022, 3110310.5331908492], [380656.762900418, 3110305.32799085], [380649.9298004271, 3110279.14619085], [380649.22760039516, 3110251.154690851], [380649.5464004191, 3110212.5712908483], [380631.822900451, 3110196.791990853], [380594.77900046733, 3110181.1313908463], [380557.01380039373, 3110161.0449908483], [380516.2542004028, 3110131.1473908504], [380508.5881004352, 3110114.8408908495], [380505.3571004279, 3110092.371490845], [380494.15750045585, 3110069.3181908424], [380484.9842004483, 3110062.1236908496], [380477.7335004356, 3110074.669190847], [380465.5036004682, 3110095.4328908483], [380461.7170004513, 3110103.837390852], [380454.3295004428, 3110107.0282908445], [380448.4422004483, 3110102.6473908485], [380445.80720045767, 3110096.2583908467], [380449.31850040826, 3110030.310390847], [380454.4973004393, 3109989.1243908466], [380450.8660004794, 3109973.8035908444], [380446.8738004584, 3109963.2441908433], [380437.0753004009, 3109953.0819908497], [380420.1739004244, 3109951.574890844], [380402.71420040197, 3109954.9551908406], [380386.16300044244, 3109961.83669084], [380373.1421004488, 3109966.893390847], [380361.8335004366, 3109965.2592908456], [380354.96910045727, 3109958.7895908477], [380342.6013003951, 3109924.5836908435], [380338.4132003938, 3109911.1676908466], [380331.47130040743, 3109908.334190844], [380321.92790045263, 3109908.1494908393], [380315.60500043374, 3109917.0880908472], [380306.12720048137, 3109933.2637908394], [380292.19690041896, 3109937.363390842], [380270.6259004269, 3109910.7876908467], [380242.926500393, 3109863.843790843], [380229.49070040946, 3109843.4956908426], [380202.78900042025, 3109818.178190843], [380158.14090039895, 3109794.4767908407], [380126.07000042236, 3109793.5620908453], [380072.3812004651, 3109790.437890836], [380005.07470040815, 3109778.7195908404], [379968.8686004536, 3109790.828390838], [379958.29820039886, 3109791.005490842], [379949.65140048123, 3109781.128090838], [379940.3184004515, 3109747.450490837], [379930.5462003996, 3109721.104590841], [379908.8406004367, 3109702.7523908396], [379881.95110039617, 3109673.7166908383], [379843.35740047385, 3109662.5714908377], [379810.59950044664, 3109669.3884908333], [379792.4221004506, 3109695.9844908346], [379794.39080047514, 3109708.5572908386], [379785.6828004549, 3109718.383390844], [379781.4600004363, 3109722.7659908426], [379739.72310040833, 3109697.637490834], [379711.6764004297, 3109691.49109084], [379687.7018004308, 3109709.124090842], [379660.7239004478, 3109752.1122908355], [379641.00340042927, 3109776.254290839], [379616.26060048124, 3109790.8447908424], [379577.74390045606, 3109786.840890844], [379547.38400040765, 3109790.282690838], [379540.23990040616, 3109774.1488908445], [379530.70990039874, 3109754.376890838], [379518.6840004212, 3109738.36429084], [379509.83620045206, 3109740.4424908436], [379500.231700457, 3109743.36819084], [379484.6867004583, 3109715.0022908375], [379470.2709004119, 3109693.6863908446], [379478.4795004461, 3109683.4673908385], [379391.21660043375, 3109632.0627908343], [379337.41050045134, 3109593.697990837], [379279.7823004732, 3109541.144890834], [379193.3609004647, 3109422.2798908274], [379063.85090045305, 3109254.486990828], [378969.071800434, 3109130.850590829], [378938.0115004588, 3109079.0004908233], [378904.3330004378, 3109018.8712908286], [378882.3558004458, 3108970.4130908265], [378883.8878004062, 3108909.374190826], [378882.6836004007, 3108868.994390821], [378850.81810043304, 3108789.482090823], [378795.19200044894, 3108747.7528908146], [378671.5790004677, 3108691.490890817], [378552.8196004508, 3108636.1913908175], [378433.97150047444, 3108581.2728908174], [378238.6225004765, 3108491.030690815], [378153.0239004514, 3108449.7749908143], [378088.36870043963, 3108451.3030908084], [377924.1943004552, 3108476.3894908098], [377910.7874004244, 3108474.126490806], [377868.814900421, 3108444.179890808], [377855.8493004541, 3108507.875590814], [377829.8443004694, 3108522.307290811], [377806.56750041014, 3108535.2247908134], [377728.20180041716, 3108574.000690813], [377628.6336004546, 3108606.7372908113], [377498.5443004649, 3108660.46459082], [377360.13550043857, 3108721.0665908153], [377326.2276004795, 3108740.1547908187], [377316.8505004145, 3108748.717590822], [377284.1334004061, 3108778.5934908176], [377204.88120047667, 3108857.5904908194], [377126.5253004384, 3108956.371690823], [377090.67390044, 3108988.4411908216], [377072.58900041267, 3108999.013890826], [377033.5388004856, 3109021.843490821], [376957.2860004161, 3109053.942690827], [376941.1153004137, 3109067.8403908242], [376905.7804004744, 3109098.208490823], [376839.3889004367, 3109236.354290824], [376797.4822004847, 3109329.8989908346], [376750.2673004655, 3109443.805590834], [376689.9543004849, 3109515.5914908345], [376566.5704004428, 3109683.580890834], [376487.1443004813, 3109768.3667908423], [376448.3114004731, 3109826.57359084], [376316.75460047234, 3109991.847190844], [376210.1245004733, 3110194.4951908463], [376164.45490048133, 3110261.0554908486], [376140.0524004301, 3110275.92669085], [376076.1512004263, 3110314.869290851], [375992.2959004182, 3110363.7754908567], [375906.94590048946, 3110409.4601908494], [375898.784400477, 3110417.8555908534], [375801.04570042447, 3110518.395690861], [375737.261100456, 3110573.180390862], [375657.2162004754, 3110654.86199086], [375531.22560042754, 3110745.8274908643], [375356.6678004185, 3110910.07989087], [375251.5186004785, 3110999.0647908663], [375129.0462004234, 3111097.213690866], [375103.6642004747, 3111114.44809087], [375044.80250044365, 3111154.4148908723], [374917.1606004147, 3111240.88159087], [374916.0745004152, 3111241.8340908745], [374878.249000447, 3111275.007290878], [374854.3879004991, 3111290.8002908756], [374777.65660045797, 3111341.5863908776], [374776.02730042697, 3111343.29839087], [374661.9456004475, 3111463.1690908778], [374651.82200043125, 3111464.0157908755], [374623.8617004786, 3111466.3545908732], [374592.19470049907, 3111483.189490878], [374498.20600049495, 3111538.5724908756], [374436.36200044927, 3111578.797990882], [374435.16580049944, 3111580.5163908745], [374413.21710043534, 3111612.0457908805], [374386.4447004787, 3111630.3733908804], [374379.187400452, 3111635.341590881], [374305.5760004167, 3111671.0887908824], [374198.2090004779, 3111675.0642908807], [374082.6644004155, 3111705.4133908823], [374019.8498005028, 3111730.912090882], [374007.3180004185, 3111743.493790882], [373984.78780049586, 3111766.113790883], [373962.1086004944, 3111817.6370908814], [373913.38530042773, 3111852.4226908847], [373868.4366005022, 3111916.6161908885], [373813.5434004801, 3111988.124990885], [373806.73120044067, 3111994.456490887], [373813.7984004753, 3111996.8271908853], [373838.8518004362, 3112005.230590887], [373845.4841004611, 3112009.0109908907], [373774.5714004929, 3112058.4651908916], [373736.8022004463, 3112092.6858908925], [373715.7554004949, 3112109.39519089], [373702.27990047174, 3112117.188290895], [373687.3364004643, 3112125.830390889], [373624.43160045054, 3112151.429690895], [373587.6598004227, 3112171.7996908897], [373583.745800436, 3112177.4948908905], [373561.9371004541, 3112209.2284908937], [373544.3241004501, 3112214.2285908894], [373530.36870050087, 3112218.190290893], [373469.2989004834, 3112219.2598908963], [373460.66870046325, 3112225.5908908905], [373457.29500045144, 3112237.376890891], [373457.18210045027, 3112237.770990898], [373466.7151004817, 3112268.6909908913], [373509.7390004611, 3112382.625790901], [373496.86880048906, 3112437.2651909], [373481.3674004449, 3112447.446390898], [373472.45750049176, 3112445.476690903], [373435.8677004651, 3112437.3879908947], [373394.855300493, 3112441.899590893], [373321.7285004405, 3112490.7408908955], [373310.01400043105, 3112499.0377908982], [373248.74550047517, 3112542.4321908946], [373188.98260046146, 3112667.431990905], [373135.9174004572, 3112754.5829909034], [373083.7955004313, 3112836.253590907], [372999.64920049685, 3112932.561690911], [372932.5398004906, 3113001.6599909123], [372906.84070045955, 3113018.897390907], [372847.9826004867, 3113058.3759909095], [372690.6042004227, 3113111.623590911], [372634.58350048633, 3113106.0751909087], [372619.26930050366, 3113098.1320909117], [372604.8893004457, 3113078.434790909], [372603.08660048345, 3113058.173190909], [372612.5169004967, 3113040.593990916], [372624.98770045774, 3113012.1111909105], [372621.40020046174, 3112986.494690908], [372612.52070050297, 3112963.771290904], [372599.024400436, 3112953.4441909045], [372579.54880049056, 3112956.9619909083], [372566.6606004839, 3112961.807790913], [372555.8391004996, 3112969.8935909066], [372553.2735004283, 3112975.2426909134], [372547.7374004222, 3112986.7849909132], [372540.5044004987, 3112994.0624909108], [372525.6549004543, 3113004.910590906], [372371.4687004249, 3113727.4706909293], [374451.67120046256, 3114686.724990945], [376653.6817004785, 3115704.1614909675], [376526.37370042223, 3116335.6597909853], [376393.11040041945, 3116953.7396909986], [376401.2824004384, 3117323.9578910093], [376561.41070042487, 3118181.2561910246], [376574.55580044055, 3118256.734191025], [376564.2658004593, 3118591.6590910326], [376579.1992004171, 3118676.205791039], [376667.24610045983, 3119136.734791048], [376892.1426004426, 3120298.328491074], [377045.2202004283, 3121059.488591092], [377255.40000043425, 3122166.1729911114], [377338.407600448, 3122550.2091911216], [377099.4536004278, 3122588.8408911205], [376637.96680044866, 3123331.650891143], [376603.5739004964, 3123370.7799911345], [376589.24560048076, 3123379.3466911404], [376567.8567004352, 3123386.8920911364], [376557.9515004898, 3123395.544691141], [376548.6742004656, 3123413.732291141], [376543.2321004369, 3123440.4197911425], [376544.9199004683, 3123457.9761911384], [376545.1859004789, 3123472.903291146], [376554.3623004237, 3123484.6863911455], [376571.0261004317, 3123496.346191141], [376598.91340047057, 3123512.14109114], [376635.9491004674, 3123541.0213911417], [376679.8499004436, 3123579.426391144], [376721.8936004322, 3123624.4391911393], [376759.86150043795, 3123639.8395911497], [376788.8674004434, 3123636.6677911463], [376819.8125004454, 3123629.8037911486], [376867.4853004556, 3123626.993791149], [376898.25320047355, 3123629.4529911405], [376920.31150042184, 3123647.6014911463], [376946.0008004727, 3123654.8856911496], [376972.2640004158, 3123658.4519911455], [376986.9883004417, 3123679.2439911426], [377008.35930047155, 3123687.0682911496], [377026.1390004371, 3123683.628791141], [377063.9243004283, 3123688.3691911474], [377145.92930049356, 3123735.721391149], [377201.3989004934, 3123756.403791147], [377217.7333004127, 3123767.8129911465], [377241.10430041014, 3123768.2639911533], [377256.6952004848, 3123754.069391152], [377275.3399004723, 3123748.7919911463], [377301.8552004554, 3123753.330391143], [377321.86280046107, 3123760.9654911445], [377348.0164004682, 3123765.0767911463], [377382.4900004143, 3123773.211891149], [377410.1532004438, 3123778.7846911503], [377439.55640042445, 3123781.038691145], [377458.9011004477, 3123781.412091149], [377482.9502004334, 3123792.1370911514], [377522.04880042403, 3123825.62709115], [377572.21090044023, 3123893.0381911537], [377596.19480042695, 3123914.5177911534], [377611.71040048276, 3123939.1882911543], [377616.44770042424, 3123955.250591153], [377628.54370044626, 3123968.905691149], [377638.0250004489, 3123971.4684911524], [377644.5037004726, 3123975.7640911485], [377647.8882004508, 3123985.9554911493], [377654.85490043415, 3123995.6201911536], [377664.996500478, 3123995.2166911573], [377673.47670045745, 3123988.239391153], [377684.84640046005, 3123986.071291154], [377692.50770042243, 3123990.389291152], [377700.2722004331, 3123989.9457911565], [377706.9574004157, 3123983.52009115], [377713.09880047047, 3123974.110491154], [377720.8398004406, 3123974.259091156], [377726.73920043034, 3123977.950191152], [377729.48730041593, 3123989.9132911526], [377739.604900482, 3123990.70669115], [377748.74710043054, 3123980.158091156], [377758.3084004199, 3123979.153391153], [377776.0520004555, 3123986.6428911565], [377795.195700468, 3123983.4419911513], [377810.1901004243, 3123966.549591155], [377829.0792004626, 3123968.264491151], [377846.8393004916, 3123981.467091152], [377862.4741004849, 3123989.169191154], [377867.3785004802, 3124007.4713911507], [377868.1382004878, 3124014.8442911557], [377873.0663004748, 3124019.424191157], [377885.4221004491, 3124014.9568911525], [377905.6155004257, 3124004.653891151], [377931.7364004794, 3123994.016291155], [377968.2230004722, 3123971.2521911524], [378004.580900477, 3123958.2923911577], [378061.8268004545, 3123936.6328911525], [378094.01390047354, 3123911.9730911506], [378125.97420045506, 3123899.528591154], [378151.39060043683, 3123888.945391148], [378174.8172004489, 3123860.0243911524], [378178.41740041506, 3123815.788391154], [378147.44600042596, 3123759.042591146], [378065.3657004552, 3123695.414891143], [377873.635300452, 3123554.103191146], [377798.640600441, 3123451.4718911396], [377800.67360047833, 3123346.282591137], [377854.3370004087, 3123294.7039911416], [377903.39670047804, 3123221.7619911395], [377921.00990045565, 3123205.966391138], [377921.92450044595, 3123183.8879911383], [377903.4772004122, 3123129.4993911367], [377895.09180046764, 3123084.841391133], [377907.9375004474, 3123040.365191133], [377997.8215004053, 3122962.0691911275], [378040.6327004485, 3122919.133891127], [378095.37640040705, 3122839.4918911313], [378157.78220043523, 3122765.1622911305], [378238.3049004373, 3122716.4327911274], [378322.20890045224, 3122651.3842911203], [378363.7127004301, 3122581.6366911214], [378389.5521004897, 3122512.3398911185], [378395.052900442, 3122464.8369911225], [378381.19180044415, 3122423.3682911214], [378362.24570048857, 3122322.41629112], [378405.53070044273, 3122229.9755911147], [378472.38710046466, 3122178.4215911147], [378530.01760042703, 3122139.9650911177], [378569.7104004193, 3122079.404791115], [378585.9885004037, 3122001.1500911075], [378595.37800042133, 3121912.6930911047], [378593.2832004573, 3121811.656391109], [378524.8029004034, 3121722.7525911056], [378457.4668004209, 3121666.771891104], [378410.9474004451, 3121582.0741911004], [378381.77300044417, 3121483.6833910956], [378341.6580004799, 3121392.5790910986], [378301.5453004059, 3121345.2049910934], [378277.8310004773, 3121292.966191091], [378257.78390041116, 3121224.9489910924], [378272.3532004149, 3121147.992391091], [378301.57370047347, 3121099.942091091], [378336.3650004891, 3121056.51969109], [378363.74990045873, 3121041.532491089], [378389.92960047704, 3121037.2060910934], [378391.54290047963, 3121150.24559109], [378392.2437004736, 3121210.2312910906], [378427.438300469, 3121262.918091091], [378478.69170045824, 3121304.610691094], [378538.5819004405, 3121341.561591092], [378607.87130047224, 3121381.645691097], [378662.5693004246, 3121414.443991097], [378717.2719004697, 3121472.748691099], [378771.9715004077, 3121545.6319910972], [378823.0271004574, 3121640.3812911063], [378820.5063004785, 3121749.1780911023], [378936.78910040576, 3121762.0213911026], [379062.54360047664, 3121740.5818911023], [379176.2887004213, 3121750.784091104], [379271.86350044364, 3121759.079891111], [379350.9772004015, 3121784.2525911042], [379407.1360004327, 3121828.3236911036], [379466.83470048336, 3121856.344591109], [379513.6898004201, 3121880.8925911086], [379563.501600401, 3121919.4673911054], [379597.26460039814, 3121953.435991105], [379624.68350046175, 3121981.906491106], [379729.456600482, 3122050.7800911088], [379742.5855004249, 3122059.4107911163], [379739.6279004629, 3122081.9681911166], [379670.9052004036, 3122381.261991124], [379741.48380045977, 3122362.1565911137], [379842.0154004032, 3122340.182491113], [380059.5064004063, 3122295.007291119], [380110.42540042306, 3122289.3844911135], [380160.46900041733, 3122276.454391116], [380185.52690040227, 3122268.1618911196], [380200.9807004653, 3122268.5666911146], [380213.18780041643, 3122276.742991118], [380224.8313004345, 3122291.0323911207], [380252.3612004784, 3122296.743991121], [380285.09320040484, 3122300.3721911176], [380344.8244004264, 3122299.312091121], [380383.6645004464, 3122291.779891116], [380439.332500433, 3122271.6884911135], [380498.632000442, 3122254.4283911195], [380552.24390046834, 3122245.341091113], [380614.26960043726, 3122229.9755911175], [380658.53000047064, 3122228.0718911174], [380682.2773004033, 3122239.5487911142], [380699.4622004027, 3122262.5232911175], [380720.4717004516, 3122283.059291114], [380747.67660042073, 3122308.746591116], [380769.92040042847, 3122322.1123911208], [380792.1683004819, 3122324.5485911146], [380806.94370043423, 3122327.7766911136], [380798.2918004778, 3122356.7775911177], [380778.09910039755, 3122414.7309911214], [380777.64520047506, 3122462.9162911177], [380783.71180040017, 3122513.0716911247], [380782.32430045307, 3122584.807891129], [380777.06940044835, 3122636.4340911224], [380757.2512004483, 3122664.9199911254], [380763.7811004788, 3122689.5415911237], [380787.12920046743, 3122704.866491125], [380811.2839003947, 3122723.705691129], [380828.45260041073, 3122741.5346911247], [380839.25680043723, 3122771.488591127], [380841.53480040503, 3122802.4453911274], [380829.94640047615, 3122844.122991127], [380827.83860047563, 3122869.987991134], [380829.2966004006, 3122923.6765911295], [380849.6067003968, 3122971.4897911362], [380854.7625004174, 3123027.74519113], [380846.492600461, 3123075.9136911333], [380842.7288004468, 3123116.505591133], [380845.91050044156, 3123157.231791137], [380858.3333004196, 3123182.268591134], [380878.75240043725, 3123204.4839911354], [380880.14320042887, 3123235.2579911384], [380864.9901004728, 3123278.2110911366], [380835.17340043536, 3123347.4721911377], [380778.3915004544, 3123461.979091141], [380747.80050042714, 3123521.0597911444], [380736.363400464, 3123546.8932911456], [380743.4781004596, 3123570.5638911477], [380771.9056004163, 3123592.701891147], [380792.0973004732, 3123620.481791146], [380795.53800047707, 3123649.939991146], [380790.1579004603, 3123678.9313911493], [380778.86060045206, 3123714.305991146], [380756.3590004771, 3123737.955791149], [380748.5347004614, 3123752.0066911518], [380747.441900444, 3123764.851991149], [380741.36220040784, 3123785.439491154], [380715.5430004735, 3123851.9029911454], [380685.494800406, 3123895.712991154], [380647.22330045776, 3123945.1535911504], [380627.35110041377, 3124007.853391156], [380623.816100462, 3124042.194991159], [380641.9474004371, 3124072.960391153], [380679.2376004241, 3124114.023091152], [380720.7032004595, 3124153.171491154], [380730.3810004555, 3124170.7043911605], [380739.04560047865, 3124196.985391156], [380718.76760044735, 3124280.061491158], [380697.3550004482, 3124335.523491166], [380669.7833004706, 3124393.9127911637], [380662.46140041074, 3124437.0158911613], [380643.8727004174, 3124516.0287911636], [380606.1127004823, 3124576.595991168], [380561.4684004809, 3124652.742891169], [380531.3144004143, 3124670.6418911717], [380521.6064004416, 3124674.292991168], [380517.69890047284, 3124683.7273911675], [380521.3127004275, 3124709.4674911695], [380526.3084004566, 3124732.517691171], [380526.5655004092, 3124756.803291169], [380510.8278004023, 3124790.374591176], [380485.00310044264, 3124833.0093911737], [380471.00880046777, 3124890.429291169], [380462.53610046895, 3124952.5361911724], [380454.1727004669, 3125003.651191172], [380453.2490004113, 3125088.61859118], [380462.4048004611, 3125124.19989118], [380460.443100443, 3125153.4209911753], [380420.67180040816, 3125199.757591179], [380405.5852004799, 3125241.0899911784], [380400.8947004704, 3125300.5759911793], [380416.94500040985, 3125392.347491189], [380419.41540044075, 3125450.7818911904], [380405.3578004552, 3125520.2968911864], [380401.63040047244, 3125580.6984911864], [380386.05460046115, 3125636.6110911923], [380379.91950040654, 3125689.3016911885], [380410.31700041145, 3125748.6591911893], [380462.168500414, 3125829.705591194], [380494.297600436, 3125906.087491197], [380501.9969003976, 3125953.581691197], [380490.734300483, 3126060.188091201], [380493.5816004133, 3126155.4998911996], [380465.3265004093, 3126242.4035912016], [380434.29250045924, 3126310.724591205], [380392.34180047543, 3126375.984491204], [380356.9394004195, 3126428.3938912116], [380332.44520040415, 3126482.5749912057], [380326.6450004531, 3126535.8893912085], [380336.4067004331, 3126596.979491212], [380342.7685004072, 3126672.0573912156], [380349.95740043547, 3126712.304491216], [380352.8858004484, 3126851.639491217], [380289.37890045694, 3126895.7894912167], [380239.83050039946, 3126943.40139122], [380176.0054004336, 3127058.7384912213], [380120.102100421, 3127099.753491222], [380044.7560004447, 3127140.391291225], [380011.28390040435, 3127194.7924912204], [380013.8408004604, 3127230.2463912256], [380068.3628004764, 3127260.6595912282], [380145.26060045447, 3127307.4787912252], [380206.1417004273, 3127344.382291229], [380204.9931004797, 3127397.7452912293], [380174.8253004051, 3127448.9724912336], [380128.71830043243, 3127496.197791229], [380095.18180048023, 3127538.0463912287], [380064.66420046205, 3127593.029291236], [380067.1773004574, 3127632.305191231], [380341.3651004516, 3127889.3347912394], [380378.11410044343, 3128051.858191243], [380461.69120046205, 3128345.166791249], [380517.6079004573, 3128479.1933912504], [380761.63800047187, 3128678.8196912585], [380760.7624004865, 3129607.4796912745], [380826.5218004421, 3130130.5485912897], [380894.774200429, 3130667.1398912976], [381028.4060004506, 3131725.6999913263], [381124.1808004023, 3132486.4221913395], [381158.6027004509, 3132759.831791346], [381161.23130045587, 3132780.70999135], [381204.9623004501, 3133128.2114913543], [381255.08680047834, 3133526.498691359], [381272.55230042734, 3133665.2908913638], [381294.7487004332, 3133841.669591369], [381297.22750043625, 3133861.53099137], [381316.30190042325, 3134014.378291371], [381354.42420040123, 3134319.879591382], [381370.55140046123, 3134446.7317913827], [381440.8668004747, 3134999.758791396], [382090.00170045916, 3135463.228091405], [382101.72660047415, 3135471.601091404], [381431.0824004095, 3136216.00309142], [381288.8826004768, 3136373.8407914247], [381133.8270004031, 3136545.9494914296], [381098.44570044754, 3136585.2212914303], [380930.19040043734, 3136771.9823914357], [380831.1479004541, 3136881.9157914375], [380756.77370045625, 3136964.4703914383], [380741.4519004419, 3136981.477491439], [380542.19020047033, 3137202.653591444], [380426.4498004388, 3137331.1212914498], [380336.56090042886, 3137430.898791446], [380137.899800467, 3137651.406191454], [380041.66130048665, 3137758.230291452], [380000.58230040804, 3137803.828591453], [379937.229000423, 3137874.14709146], [379755.05200048664, 3138076.3618914653], [379734.02070041606, 3138099.704591466], [379529.1648004808, 3138327.090991466], [379422.14420041634, 3138445.879391467], [379405.65210044256, 3138448.9607914737], [379399.45190041955, 3138450.119891472], [378758.85770041466, 3138569.8020914765], [378516.7568004822, 3138615.032891478], [378223.6381004647, 3138669.79749147], [378146.0097004756, 3138684.302491475], [377870.85060047405, 3138735.709491479], [377787.17370044254, 3138751.3433914725], [378084.677100422, 3139011.9517914797], [378187.4176004238, 3139101.951491485], [379361.0264004927, 3140120.2354915077], [379374.41280042543, 3140131.8519915114], [379710.5835004328, 3140423.531091515], [380073.7575004695, 3140738.639791523], [380401.46750041994, 3141022.9793915297], [380519.64780048025, 3141150.1187915294], [380717.11510044656, 3141440.909191533], [380660.27130048466, 3141532.7884915397], [380569.98310041515, 3141678.720091545], [380537.9756004249, 3141700.8519915426], [380427.64690041996, 3141777.1494915416], [380426.5324004877, 3141886.4639915447], [380425.44980042544, 3141992.6400915463], [380248.9412004746, 3142002.41819155], [380197.85260044644, 3142005.2503915443], [380160.96760046505, 3142175.495391551], [380134.4656004853, 3142297.810691552], [380090.4012004307, 3142391.254291558], [379997.3623004583, 3142588.5470915656], [379950.22350043093, 3142688.511591566], [379885.9265004025, 3142764.1426915666], [379750.286200415, 3142923.699691572], [379663.11990040785, 3143106.379191578], [379658.5618004648, 3143115.9329915717], [379654.33550047217, 3143124.790791572], [379640.89040042646, 3143152.9699915736], [379676.5184004243, 3143207.495991578], [379652.1035004796, 3143261.0134915793], [379608.7632004627, 3143359.7419915767], [379593.42440045264, 3143394.7053915747], [379574.8048004903, 3143437.148591575], [379567.7861004256, 3143453.14659158], [379364.86260041804, 3143915.6990915914], [379181.43170048774, 3144111.1891915877], [379042.1494004084, 3144145.4905915936], [379004.2848004568, 3144200.8708915976], [378957.00890042156, 3144237.698891595], [378902.37920043827, 3144312.370391595], [378837.237000467, 3144239.3113915995], [378720.36410044297, 3144238.680391593], [378688.897800433, 3144281.636291595], [378659.88570046565, 3144286.921191597], [378634.69030048663, 3144297.814791597], [378612.4414004884, 3144321.998291595], [378601.196600415, 3144333.732291596], [378586.58380049135, 3144340.6830915962], [378566.4082004269, 3144342.181791596], [378529.05040043633, 3144341.7976915953], [378475.07380048744, 3144371.190591604], [378477.9609004937, 3144402.4718915974], [378488.27320044104, 3144432.592891602], [378504.7261004819, 3144475.493191604], [378505.05250048795, 3144508.589391602], [378494.4927004172, 3144539.2257916024], [378480.61680041597, 3144578.2014916013], [378466.6684004641, 3144601.9718916006], [378459.81860045134, 3144609.9042916056], [377905.21470046835, 3144867.061791613], [377871.4971004621, 3144854.3313916097], [377830.5606004286, 3144832.8907916127], [377785.5932004112, 3144816.2880916125], [377757.27590048045, 3144805.005591606], [377716.28610044747, 3144800.649291612], [377690.6314004989, 3144787.023491609], [377653.9230004806, 3144772.351191609], [377603.4828004736, 3144754.5846916037], [377200.466200486, 3144458.192591605], [376487.77710045734, 3143996.198491595], [376420.1748004316, 3143946.364691596], [376331.7731004473, 3143880.794091588], [376261.4648004963, 3143854.418991589], [376170.35810050386, 3143812.310591586], [376063.5595004187, 3143780.567791589], [375967.2031004329, 3143746.2616915866], [375933.36440048396, 3143730.4727915837], [375876.00930044975, 3143725.0172915887], [375818.66590048023, 3143716.953591586], [375748.1828004961, 3143732.3072915804], [375706.37830045365, 3143750.3909915877], [375651.48910047626, 3143778.8514915863], [375580.9200004193, 3143815.069091587], [375539.0287004558, 3143854.01749159], [375471.1653004906, 3143866.7744915886], [375392.8923004904, 3143874.272091587], [375291.18990047666, 3143871.2406915873], [375181.6845004223, 3143862.95949159], [375072.1261004724, 3143867.718891589], [374988.602600459, 3143883.0192915928], [374881.58720046317, 3143903.4373915857], [374756.3791004835, 3143908.1319915904], [374584.06410043273, 3143951.7497915947], [374578.82620046206, 3143956.945991589], [374521.4827005048, 3143948.8818915877], [374453.6956004666, 3143943.382591589], [374411.9011004686, 3143958.8568915874], [374372.72720050777, 3143971.734691592], [374320.5227004947, 3143981.9480915936], [374265.731100492, 3143986.9357915893], [374218.83080050343, 3143976.3095915886], [374148.0277004908, 3143980.304191589], [374070.52010046167, 3144075.3200915894], [372717.9452004777, 3145641.749891622], [372054.85500049026, 3148756.630691695], [373161.3775004539, 3150616.2388917324], [373167.38870049483, 3150628.171591731], [373146.3210005122, 3150648.1497917315], [373130.4309004506, 3150676.646791737], [373096.4685005053, 3150717.152391733], [373007.66510048514, 3150806.2247917405], [372958.01830048545, 3150885.238691741], [372949.77190043975, 3150921.72389174], [372962.42170048004, 3150944.00879174], [372955.2943004605, 3150968.6105917464], [372926.3958004549, 3151001.4536917447], [372839.1466004766, 3151077.1977917473], [372804.76270049246, 3151080.334491741], [372774.8727005097, 3151071.3363917456], [372750.9137004618, 3151055.6065917388], [372718.0673004584, 3151041.6838917416], [372702.9406004905, 3151053.5526917432], [372668.0817004594, 3151098.099591741], [372640.8014005162, 3151126.284091741], [372621.37080050795, 3151142.7639917424], [372603.13630046643, 3151144.291291749], [372583.92820048553, 3151141.0874917456], [372572.15520049643, 3151126.942391741], [372576.18360045005, 3151101.8708917466], [372573.31450043543, 3151089.0887917485], [372543.7038004738, 3151060.615291744], [372509.9460004596, 3151056.6629917473], [372501.48470047954, 3151068.398791743], [372497.8324004416, 3151093.927291745], [372492.33700050105, 3151160.490491742], [372478.134700488, 3151182.636191746], [372440.26670044614, 3151218.7227917477], [372411.9852005023, 3151240.841791748], [372410.67530047597, 3151256.462591749], [372398.48210044205, 3151274.8777917502], [372353.6108004942, 3151302.258791745], [372328.5127004483, 3151331.8609917485], [372213.8799004947, 3151419.81869175], [372138.9943005209, 3151441.76229175], [372048.7666004652, 3151556.591991754], [372017.0508004946, 3151561.9481917517], [371987.59380049194, 3151563.723791755], [371983.2863004521, 3151577.054791753], [372005.0347004627, 3151597.899991756], [372022.80060048774, 3151620.4906917573], [372022.31000049924, 3151646.121291756], [371985.64140048606, 3151709.819591758], [371983.300500502, 3151727.6159917577], [371976.8206004702, 3151736.820791758], [371964.59070043906, 3151746.277791758], [371944.93530045135, 3151807.095991763], [371921.568900447, 3151886.4547917596], [371898.5379004994, 3151924.243291762], [371870.8363005046, 3151937.417191765], [371832.76170051843, 3151935.7555917613], [371803.7885005006, 3151960.0744917663], [371786.48810049484, 3151985.552691763], [371781.3277004606, 3152007.898891763], [371783.4228004897, 3152037.877291761], [371765.179600504, 3152059.4851917634], [371781.1616004478, 3152074.7956917686], [371795.21610049834, 3152067.7842917624], [371814.39500049636, 3152070.1370917703], [371820.7568004803, 3152084.1573917656], [371831.9970004667, 3152085.6970917634], [371848.11320050486, 3152103.6369917644], [371857.2957004962, 3152114.643591769], [371856.8007004685, 3152140.4492917685], [371830.9879004903, 3152149.4759917655], [371824.43010045146, 3152187.589291771], [371815.61430047866, 3152213.1888917647], [371817.7460005106, 3152232.348291772], [371833.9441004746, 3152255.9331917693], [371836.1712004713, 3152270.1061917683], [371814.4211005081, 3152275.5093917726], [371773.3135004833, 3152263.2331917672], [371752.1609005222, 3152267.8564917687], [371723.8437005215, 3152300.5148917725], [371706.62710047024, 3152354.7769917715], [371690.26910045434, 3152375.4746917714], [371668.228100473, 3152367.5660917675], [371645.46630043956, 3152346.0123917735], [371626.86870046635, 3152303.9073917684], [371618.106600448, 3152252.438791769], [371603.31120047945, 3152239.6408917727], [371585.69480050704, 3152235.927191772], [371528.06190050405, 3152286.5010917713], [371480.2445004761, 3152291.8197917757], [371403.18500045885, 3152285.0176917682], [371385.07160049694, 3152297.7055917648], [371376.3534004683, 3152317.369291773], [371371.7522004609, 3152353.9533917685], [371372.19940047147, 3152420.3151917765], [371379.417400505, 3152482.133691772], [371394.7893004664, 3152534.6522917734], [371420.39570050314, 3152586.3176917788], [371417.12420043856, 3152622.664491776], [371403.8214004808, 3152636.9274917752], [371386.47300048434, 3152653.0089917784], [371375.5925004947, 3152698.151091781], [371364.82930044614, 3152706.599791781], [371366.28900048457, 3152721.6321917754], [371401.8112004564, 3152738.263091777], [371395.5891004954, 3152798.024691782], [371387.8584004829, 3152827.375991786], [371380.1185004716, 3152859.0056917807], [371375.75560051744, 3152928.526191785], [371348.89340049156, 3152946.1257917816], [371316.0867004703, 3152951.7098917877], [371295.8424005231, 3152971.024491786], [371299.94410047244, 3152995.4258917854], [371312.42220051045, 3153055.8150917892], [371308.41060049983, 3153095.067791788], [371273.99000050296, 3153123.0702917906], [371224.9937004728, 3153179.4987917934], [371223.2367004739, 3153206.495291792], [371235.60490047454, 3153222.801091795], [371263.683500494, 3153233.563591792], [371299.85990050924, 3153227.626691788], [371355.088800493, 3153198.0809917925], [371425.96970045374, 3153179.796791791], [371460.0128005113, 3153158.0652917842], [371506.41270044027, 3153143.039191792], [371547.03800045245, 3153200.985291794], [371566.11010049446, 3153255.519291789], [371545.12510050304, 3153295.8959917943], [371523.6645004754, 3153344.410491795], [371514.01080044126, 3153395.196191797], [371524.521800501, 3153414.405791795], [371556.6076004582, 3153407.552491796], [371575.7365005156, 3153367.186091796], [371591.44680045947, 3153363.4140917906], [371611.2236004926, 3153393.076291794], [371636.1649004945, 3153434.544591799], [371668.4787004825, 3153478.7758917995], [371714.7055005088, 3153494.6135917976], [371778.69900049386, 3153546.412491796], [371784.3282004588, 3153620.383591804], [371770.54670044675, 3153651.246791797], [371750.17040050676, 3153691.5910918023], [371760.2527005049, 3153748.1648917976], [371785.90630049934, 3153786.2358918], [371825.89550050977, 3153833.4775918047], [371854.3915004636, 3153866.0048918007], [371847.07290046196, 3153907.303691807], [371822.276800478, 3153960.882791803], [371821.80240047304, 3153985.6777918073], [371830.0783004941, 3154032.7457918045], [371858.45730047923, 3154071.188491805], [371865.94380044646, 3154116.4357918114], [371860.7140004396, 3154144.9770918074], [371850.575200521, 3154172.5225918153], [371834.9639004958, 3154196.6593918134], [371836.7677004723, 3154223.198191811], [371844.4043004957, 3154267.679191811], [371857.1205004557, 3154347.6333918185], [371865.9935005, 3154400.6590918163], [371870.02910044685, 3154457.540491818], [371854.75090046885, 3154501.1367918183], [371885.0482004882, 3154511.3112918218], [371897.2649004408, 3154534.313391821], [371883.089800481, 3154562.299791824], [371854.17700047157, 3154583.8245918187], [371847.37380047067, 3154609.33919182], [371850.0702004595, 3154630.9370918185], [371863.21110047784, 3154631.625891826], [371885.7255005173, 3154623.738591818], [371905.4379004771, 3154601.78769182], [371926.20600044867, 3154593.1771918223], [371959.54360047367, 3154592.885691822], [371981.9669004519, 3154599.6179918237], [372009.1560005215, 3154629.9845918203], [372029.26220049005, 3154658.8004918215], [372036.7342005094, 3154684.5771918204], [372029.7460005037, 3154702.750091822], [372013.992900491, 3154715.81809182], [371986.8388004601, 3154725.3712918223], [371983.2353004845, 3154756.204291826], [371967.44070046395, 3154769.040091823], [371929.1766004807, 3154758.0458918214], [371891.2776004467, 3154762.3920918284], [371871.70180047903, 3154799.3443918247], [371841.6846004771, 3154834.6797918295], [371832.67570051184, 3154885.064791829], [371821.0081005234, 3154911.9899918297], [371750.15610047436, 3155001.2795918332], [371721.86220047704, 3155017.420491829], [371683.98610045627, 3155068.6618918343], [371638.9905004784, 3155081.9092918322], [371622.25320046843, 3155095.1082918337], [371622.33290044207, 3155115.36949183], [371640.37970051816, 3155122.407191834], [371652.0915004414, 3155142.72969183], [371642.06080052647, 3155162.6581918313], [371615.2296004535, 3155173.956291833], [371602.16510048165, 3155161.15739183], [371577.77740049025, 3155160.6892918325], [371549.38670050923, 3155180.281291831], [371515.27170046733, 3155185.498191833], [371475.07080051466, 3155186.0555918296], [371457.4829005054, 3155216.83809183], [371441.6031004598, 3155221.786891838], [371418.749900509, 3155213.0800918387], [371393.41830046196, 3155233.934291832], [371374.9809005191, 3155277.1992918393], [371340.0923005091, 3155311.55339184], [371346.69430052105, 3155330.8821918354], [371323.7073005035, 3155340.410191839], [371291.09740049095, 3155359.844091837], [371247.488300501, 3155363.4526918363], [371154.25410050864, 3155349.568991838], [370986.7307005051, 3155351.3022918366], [370956.91780045844, 3155313.056891834], [370918.8282005096, 3155304.9596918393], [370876.2155004693, 3155320.34259184], [370810.23620046256, 3155303.5864918334], [370747.4275004675, 3155268.582691837], [370707.84510051174, 3155236.135791832], [370639.22130049084, 3155241.8594918335], [370571.17820050113, 3155234.9786918294], [370488.28880045254, 3155240.3019918357], [370433.00640047074, 3155224.378591834], [370396.8425004523, 3155194.944591837], [370373.1303005127, 3155159.4014918273], [370316.1910004725, 3155148.396991836], [370284.56430047203, 3155130.32699183], [370242.7560005049, 3155069.6099918326], [370217.26180051774, 3155026.1924918243], [370202.55270052806, 3155000.7650918276], [370167.9248005105, 3154995.730191827], [370116.10000050423, 3155005.3900918313], [370060.52430049627, 3154991.9404918314], [369983.1563004542, 3155046.402791828], [369892.030500443, 3155198.6536918324], [369841.5050004752, 3155292.767991833], [369855.7839004452, 3155356.8659918425], [369876.5402004804, 3155418.589591842], [369874.5364004428, 3155489.820591836], [369883.03830046306, 3155511.605291837], [369904.72820052755, 3155533.004691836], [369911.9735005197, 3155552.144891841], [369911.91520047444, 3155582.4830918363], [369907.2673005243, 3155617.733291839], [369905.94980052544, 3155653.832091847], [369917.05730048416, 3155703.5672918437], [369920.9897004612, 3155754.8791918466], [369937.7275004663, 3155812.7244918444], [369926.6419004712, 3155839.942391851], [369896.01720053144, 3155866.785091848], [369868.5468004439, 3155880.088091847], [369836.62710049446, 3155887.9218918476], [369830.26430048916, 3155918.251191853], [369838.4775004502, 3155965.1992918514], [369860.3477004748, 3156010.4291918525], [369876.1950004472, 3156058.751091857], [369856.7583005141, 3156084.6975918566], [369809.8419005281, 3156103.2039918494], [369787.2700005075, 3156151.148491852], [369757.66140046844, 3156173.313991856], [369757.4749005155, 3156212.5096918554], [369748.0009004526, 3156250.4876918574], [369731.65110049164, 3156290.498991855], [369706.23480052676, 3156313.216391854], [369683.94350050297, 3156356.2934918622], [369677.5894004437, 3156401.014091856], [369664.9801005158, 3156437.3791918606], [369642.38810044865, 3156462.6872918615], [369605.1318004984, 3156480.219691862], [369586.6481004912, 3156497.4914918607], [369574.75920050096, 3156523.1838918612], [369565.36940050113, 3156562.921991866], [369558.2716004668, 3156597.5570918596], [369560.6099005053, 3156625.052791864], [369574.4558004509, 3156657.914791867], [369582.2814005044, 3156679.5184918647], [369595.8713004689, 3156704.933291865], [369606.5936004667, 3156734.1188918655], [369616.73250047973, 3156758.981491866], [369637.64420048904, 3156784.205291864], [369646.7416005119, 3156806.50639187], [369642.1823005193, 3156853.6406918713], [369649.02860048827, 3156879.9759918684], [369675.52650049166, 3156910.3670918737], [369708.19510052237, 3156931.5542918686], [369725.1894004446, 3156951.4505918706], [369738.0334004483, 3156978.217991868], [369745.1174004822, 3157027.7517918698], [369743.2605005217, 3157063.8455918753], [369719.9499004613, 3157112.558991879], [369700.7589004763, 3157150.737991872], [369637.8806004493, 3157204.4109918764], [369613.88650046004, 3157236.201991877], [369619.8226004829, 3157266.1355918758], [369649.08100049105, 3157279.320891877], [369674.9400005058, 3157276.0470918803], [369673.75840052776, 3157308.5131918807], [369659.20340047125, 3157326.7032918804], [369639.0634005063, 3157353.6686918805], [369638.19930048357, 3157398.9246918797], [369625.0597004544, 3157436.503591884], [369637.9849004551, 3157485.2244918835], [369650.325600446, 3157557.347991885], [369653.3409004825, 3157631.5354918875], [369657.8501004656, 3157691.33039189], [369681.26340047346, 3157724.852991885], [369751.16510050104, 3157745.042691893], [369801.2451004623, 3157747.6935918885], [369870.31140044506, 3157740.4268918918], [369908.8514004478, 3157727.0187918874], [369921.34290046565, 3157686.268091888], [369938.16310052335, 3157640.2865918833], [369946.4773004476, 3157608.547091886], [369929.120500466, 3157579.6807918833], [369903.42960049806, 3157555.776191887], [369924.57960047014, 3157513.7115918817], [369956.8681004571, 3157478.56149188], [369991.5308005102, 3157450.204591884], [370015.6223004825, 3157464.8775918824], [370049.3860004446, 3157477.7954918817], [370108.2361005105, 3157483.3692918858], [370116.66520047927, 3157518.256591883], [370103.4319005262, 3157563.3967918837], [370081.857700514, 3157633.563591884], [370087.45960049896, 3157669.057291884], [370112.3884004975, 3157702.4009918873], [370142.8397004904, 3157707.3352918867], [370167.13870049536, 3157710.136991885], [370178.7261005194, 3157744.9349918896], [370173.11270046025, 3157768.761091891], [370174.5892004764, 3157798.367491891], [370178.845400486, 3157834.493291889], [370163.54840048566, 3157839.7467918918], [370142.2954004546, 3157830.4464918924], [370122.23800045333, 3157839.520391893], [370109.67370046163, 3157871.0807918967], [370113.9252004988, 3157896.5042918925], [370125.70020051365, 3157912.2588918945], [370151.1246005193, 3157922.182291893], [370174.245500453, 3157922.8250918896], [370201.35010048, 3157931.3458918887], [370205.70890051237, 3157948.898191896], [370205.4817004708, 3157975.2333918917], [370223.79540051566, 3157994.918491893], [370224.3486004773, 3158010.426291891], [370209.3217005265, 3158022.915091897], [370179.155400518, 3158029.4112918978], [370154.96410046227, 3158039.6389918956], [370130.9465005189, 3158066.434891897], [370130.7599005044, 3158086.2493918925], [370147.3531005131, 3158106.981691897], [370206.5821004593, 3158121.177391893], [370240.75310046657, 3158106.9696919005], [370304.61390048754, 3158096.6324919], [370322.3697004988, 3158119.261591892], [370326.21830052166, 3158152.5517918947], [370332.08140045777, 3158189.529891895], [370339.13620044576, 3158254.1215918968], [370322.6572005048, 3158275.6187918973], [370281.05340045725, 3158278.7128919023], [370231.2019005067, 3158282.437091898], [370225.383400513, 3158302.032291902], [370229.8649004936, 3158328.117091904], [370283.27840048133, 3158372.3048919044], [370324.99210048513, 3158398.991791898], [370353.82610051415, 3158422.1854918995], [370347.04190049693, 3158487.990791904], [370332.62170047616, 3158541.0626919013], [370363.6543005059, 3158560.4676919053], [370371.44520045916, 3158605.8052919093], [370364.5686005181, 3158643.16899191], [370390.0782004996, 3158680.2533919117], [370424.93320044386, 3158712.3265919117], [370428.28350049874, 3158793.4418919105], [370414.0474005042, 3158831.7224919153], [370392.736500464, 3158866.580691919], [373380.09090045746, 3159968.536391942], [372867.73770048004, 3160590.459491952], [372841.87390049885, 3160607.165891948], [372810.61800048314, 3160626.1438919473], [372778.9388004703, 3160636.2137919515], [372743.559900464, 3160653.332991956], [372708.1720005146, 3160671.045191948], [372679.31460045284, 3160688.8804919575], [372645.2744005214, 3160710.323791956], [372621.9055005045, 3160740.764391955], [372601.17100046144, 3160774.536191955], [372587.6193004818, 3160810.5426919567], [372581.17670044524, 3160830.8194919606], [372567.1715004479, 3160850.9502919596], [372541.575200497, 3160883.7047919575], [372521.75670047157, 3160930.9227919634], [372501.72180044686, 3160985.763991964], [372499.53970047564, 3161020.0423919586], [372474.55110050645, 3161048.5460919635], [372418.2712004453, 3161075.6875919653], [372432.3516005014, 3161179.935791968], [372417.8940004388, 3161226.4553919616], [372405.5087004854, 3161272.016991967], [372356.3223004538, 3161311.736391971], [372261.0959004394, 3161341.784191965], [372228.4579004665, 3161375.6644919673], [372246.5070004448, 3161408.6506919703], [372265.1400005159, 3161448.1906919708], [372266.53850052215, 3161515.073491971], [372287.191700439, 3161577.2604919733], [372292.75530047156, 3161628.9785919744], [372151.15770045365, 3161756.2587919733], [372085.68990047567, 3161843.688391976], [372061.0156005038, 3161908.215391978], [372005.8407004862, 3161940.500891977], [371976.95140045474, 3161955.123791981], [371985.4484005255, 3161996.0740919816], [371978.66480049107, 3162029.2747919834], [371948.1417004694, 3162073.81869198], [371942.2155005166, 3162101.9558919817], [371924.2671004599, 3162131.747091985], [371922.22250051587, 3162172.7017919817], [371922.24010049197, 3162240.5760919875], [371922.7744004715, 3162294.254991991], [371908.6079004925, 3162332.6317919837], [371881.7448004711, 3162371.1563919936], [371837.70080047013, 3162380.549991995], [371779.34440050746, 3162378.84629199], [371728.48470044835, 3162385.9135919935], [371697.93680045573, 3162425.526091991], [371686.30280045635, 3162471.5936919935], [371684.83730046067, 3162540.385191996], [371661.095200506, 3162596.446791991], [371590.8559004492, 3162658.911391996], [371559.178100441, 3162674.9411919974], [371548.9043004844, 3162708.243691999], [371557.1703004626, 3162745.2324919985], [371576.4795005262, 3162785.9951919983], [371623.092800488, 3162814.7354919985], [371632.4185004735, 3162832.0786920027], [371620.6691004535, 3162859.608392005], [371556.57330050546, 3162918.519792003], [371495.44940051483, 3162989.4399920027], [371456.9044004575, 3163032.0931920074], [371451.2099005264, 3163091.6051920033], [371423.8159005244, 3163115.5957920076], [371376.82930046733, 3163120.737292002], [371333.2736004929, 3163123.5497920047], [371279.65890049003, 3163101.865492003], [371266.5311004541, 3163112.4639920034], [371265.76240047347, 3163135.4165920033], [371247.37500046624, 3163164.7340920055], [371223.74610051315, 3163189.338692011], [371164.65730051347, 3163194.245192012], [371130.74100044614, 3163170.4088920094], [371106.56240044226, 3163171.8021920105], [371080.7425005182, 3163195.65559201], [371063.7723004458, 3163234.868992011], [371059.91600048315, 3163273.2553920057], [371079.3365004955, 3163325.28039201], [371048.70330046955, 3163358.3167920127], [371017.8533004809, 3163383.7228920134], [371016.00260048464, 3163409.806792011], [371010.5542004974, 3163478.4541920098], [371031.85180050984, 3163522.156192012], [371055.9017004942, 3163582.1209920156], [371048.89330049645, 3163592.971592013], [371035.1908005179, 3163602.215892014], [371007.8927005117, 3163612.169792016], [370975.37760050653, 3163611.933092012], [370947.26370050095, 3163605.2816920136], [370919.5455005257, 3163584.872892015], [370893.0676004591, 3163587.4298920166], [370874.35490050033, 3163612.822192019], [370844.7737005076, 3163627.177592015], [370795.1018005035, 3163630.1293920185], [370755.3430005249, 3163642.9530920135], [370714.8256004949, 3163653.6098920135], [370723.44460051466, 3163704.0293920184], [370669.7319004937, 3163725.05699202], [370631.4380004867, 3163724.733292021], [370592.3117004888, 3163741.7369920244], [370567.9359005256, 3163727.8466920163], [370565.0912004666, 3163726.300092018], [370540.74410048046, 3163741.7952920166], [370503.2556004681, 3163744.8718920164], [370479.76920049207, 3163772.120592016], [370441.5426005182, 3163767.26889202], [370410.8594005069, 3163776.970192021], [370388.09800048085, 3163775.606592022], [370294.468000519, 3163915.54559202], [370336.25930049754, 3163967.016892024], [370377.35850045667, 3163995.603792028], [370363.84510052553, 3164009.719392023], [370330.7325005206, 3164021.655392023], [370329.2475004689, 3164039.365592021], [370329.9233004511, 3164063.9843920227], [370342.9879005024, 3164089.3479920253], [370325.6319005216, 3164109.270892029], [370288.7360004523, 3164142.234892024], [370276.6405004727, 3164142.6405920237], [370266.6586004486, 3164132.284692029], [370247.5659004798, 3164132.556292022], [370223.1933005038, 3164154.0186920315], [370194.7966004955, 3164152.9428920266], [370164.77070046717, 3164127.820792026], [370115.77660048543, 3164118.234892028], [370039.20470047905, 3164184.8679920295], [369986.6308005203, 3164277.3683920274], [369951.67430051893, 3164316.9852920324], [369915.531100518, 3164342.54539203], [369873.8111004783, 3164355.15129203], [369808.6269004785, 3164344.1676920312], [369789.1212005255, 3164317.926492034], [369780.934000467, 3164291.0895920326], [369755.2530004507, 3164281.894092032], [369726.0021004923, 3164291.9092920343], [369733.58000051917, 3164330.7774920287], [369729.7326005014, 3164361.698992027], [369718.5667004794, 3164406.3087920356], [369699.3011005207, 3164411.652992034], [369680.0296004723, 3164459.8404920343], [369659.16090047295, 3164543.7293920317], [369610.7152005056, 3164582.2010920364], [369566.2337005035, 3164605.171292036], [369511.8922005322, 3164647.402692034], [369495.125400524, 3164725.3974920376], [369438.5403004987, 3164754.8284920426], [369388.47310050204, 3164763.0291920453], [369331.68410045793, 3164749.741592041], [369278.49360048654, 3164749.481392041], [369212.1470005286, 3164790.8067920385], [369161.7289004779, 3164805.383092039], [369101.40020052134, 3164745.3920920407], [369042.6042004582, 3164726.8878920404], [368957.55700051336, 3165052.0803920506], [368909.5753004526, 3165136.733592046], [368877.27470053395, 3165147.945492045], [368790.16230053396, 3165247.060392053], [368745.5698004544, 3165272.9463920523], [368672.3981004964, 3165249.8003920545], [368599.6697005158, 3165252.0522920503], [368550.5944005359, 3165261.617392049], [368506.43530051643, 3165212.64899205], [368455.4361005004, 3165205.764492047], [368418.09290048666, 3165228.37089205], [368380.19420048385, 3165236.8767920514], [368358.2486004672, 3165216.4655920486], [368348.65260048764, 3165192.519792053], [368328.5810005217, 3165145.12269205], [368256.0780004518, 3165169.0973920547], [368226.4945005253, 3165166.8407920515], [368188.04580045224, 3165213.6868920503], [368146.99080053036, 3165226.3093920457], [368099.34510047885, 3165173.5762920436], [367864.9992005414, 3165130.5881920476], [367894.0632005392, 3165276.0449920488], [367952.9046005092, 3165398.398392049], [367945.9744005301, 3165588.81069206], [367918.1945005211, 3165639.8381920583], [367861.5152004558, 3165641.9589920584], [367811.65260045463, 3165622.8702920633], [367764.34250047756, 3165637.9740920556], [367643.65290047857, 3165746.6468920647], [367628.9339004556, 3165790.1138920654], [367580.5768005332, 3165804.1309920656], [367523.1718005082, 3165844.7691920614], [367482.706000479, 3165918.1955920653], [367414.69790052075, 3165982.4730920657], [367376.20660053735, 3165999.688192066], [367309.2134005197, 3165988.5354920696], [367281.3006004838, 3166038.722892065], [367257.4826004858, 3166086.8691920685], [367199.22510051203, 3166076.8445920646], [367113.23580053786, 3166073.586092065], [367057.3681005136, 3166153.6254920685], [367007.74320053874, 3166200.4390920717], [366963.0817005109, 3166245.050992067], [366950.55110050784, 3166329.060592077], [366949.9107005047, 3166328.9020920694], [366880.18580046145, 3166311.6487920727], [366879.95340049814, 3166311.742592073], [366832.0147005423, 3166331.09589207], [366796.7011005039, 3166378.15299207], [366780.90610051143, 3166426.645792075], [366777.0600005046, 3166478.6325920755], [366804.4701004885, 3166597.5556920823], [366820.3037004841, 3166665.3425920843], [366759.32340054226, 3166710.150192082], [366718.4794004847, 3166740.359992082], [366678.35210053046, 3166769.6985920807], [366625.010300463, 3166805.9146920852], [366566.26240054367, 3166843.487092085], [366518.1549005335, 3166885.3110920866], [366526.49980054377, 3167003.178092086], [366530.1684005278, 3167119.810792092], [366506.2677004893, 3167203.303892097], [366426.3930005204, 3167286.5987920933], [366380.71920052846, 3167303.8408920984], [366335.60110051575, 3167360.8600920946], [366054.7274005228, 3167665.9313920983], [365974.1837004742, 3167757.953192101], [365928.62660052744, 3167842.845392106], [365846.03260054387, 3167892.7600921053], [365320.842800546, 3168351.271492117], [365262.49130048614, 3168446.689892122], [364863.03070054913, 3169210.0293921367], [364703.43810054404, 3169488.8533921423], [364593.9497004859, 3169728.972992143], [363021.95080052956, 3170728.9431921723], [363011.19290053594, 3170762.3030921645], [363000.27570052975, 3170849.4596921727], [362993.0730004937, 3170958.583592171], [362995.42920051294, 3170991.688592169], [362996.56180049025, 3171051.96309218], [362950.83490053355, 3171137.4660921735], [362808.4608005112, 3171261.549692181], [362754.8241005468, 3171286.2434921805], [362710.58640048, 3171333.171592179], [362688.8781005569, 3171408.5924921837], [362680.7728005588, 3171507.073292185], [362582.5523004859, 3171562.341392188], [362532.245900478, 3171634.680592187], [362443.10820050654, 3171665.5668921857], [362423.3483005402, 3171712.710892189], [362301.35220055346, 3171981.3292921917], [362311.3802004882, 3172094.137192194], [362296.0498005003, 3172172.214292201], [362205.23160055437, 3172257.3565922007], [362258.37740055996, 3172404.7220922024], [362254.67740047537, 3172470.471892208], [362200.24680050986, 3172678.005192214], [362230.6645004896, 3172746.4395922087], [362191.7759005148, 3172790.561892216], [362148.56940054736, 3172791.157792213], [362022.0452004989, 3173151.2646922246], [362015.3196005017, 3173196.7083922224], [362032.55880055146, 3173243.199592221], [362075.1819005507, 3173286.296392227], [362050.44430049666, 3173367.141792223], [361989.4898005016, 3173456.768392227], [361974.0379004942, 3173539.3169922247], [362002.5192005215, 3173722.3903922327], [361972.9652005191, 3173779.681792238], [361934.3016005454, 3173824.264792235], [361867.53010056005, 3173847.742692238], [361757.5670005324, 3173872.3868922316], [361743.77560053207, 3173969.084692237], [361560.1300005658, 3174232.7553922436], [361538.5329005625, 3174344.3475922467], [361562.52770056203, 3174453.179592247], [361504.9461005217, 3174468.679192248], [361432.1245005165, 3174474.072692246], [361303.66690049414, 3174579.290692245], [361229.64100055746, 3174604.045792256], [361090.7726005365, 3174564.3414922524], [360981.5981004882, 3174603.8018922554], [360902.5803005094, 3174652.784192253], [360863.43610049656, 3174787.744492262], [360807.64030049636, 3174888.6015922567], [360705.8188005513, 3174910.96039226], [360617.9936005355, 3174926.4768922618], [360486.808800522, 3175032.572692265], [360406.80460049, 3175137.2370922663], [360361.24230056, 3175284.7403922686], [360387.76320051716, 3175480.3797922675], [360409.3639005127, 3175567.627592274], [360421.4100005174, 3175640.9864922767], [360414.84390049626, 3175696.448092273], [360409.25160052965, 3175746.4941922817], [360423.5326005302, 3175790.6925922763], [360413.3715004885, 3175807.1438922742], [360384.0758005574, 3175833.8237922764], [360353.7361005432, 3175916.3722922755], [360352.3509005158, 3175989.600692279], [360343.34750057023, 3176052.067792284], [360322.91000055673, 3176102.084792285], [360305.2970005551, 3176110.3448922876], [360292.8710005468, 3176162.2729922873], [360258.15850056947, 3176192.606592286], [360273.53050053737, 3176188.535592285], [360255.8668005598, 3176202.092592288], [360251.6064005053, 3176217.687592285], [360242.29900051106, 3176262.6463922914], [360196.6054005006, 3176303.3529922892], [360139.02920053597, 3176334.7769922884], [360073.6721005455, 3176355.5296922917], [360013.0841005456, 3176370.258792293], [359992.99720054306, 3176393.9211922893], [359967.24210055, 3176470.7861922933], [359967.3345005247, 3176506.098392292], [359973.7524005382, 3176533.55589229], [359997.3791005331, 3176590.804892293], [359983.6893005447, 3176631.3017922943], [359973.8142005234, 3176642.3186922944], [359947.78930056165, 3176663.608992297], [359927.60970050225, 3176671.948292297], [359906.9361005038, 3176671.9452922936], [359869.7161005348, 3176697.8830922926], [359853.41970051825, 3176705.288092293], [359816.35310056794, 3176698.651592292], [359796.35900056746, 3176697.4038922945], [359729.4162005303, 3176716.5618922976], [359703.8410005482, 3176711.2978922944], [359684.54540053377, 3176696.1603922946], [359667.73570056254, 3176695.413192294], [359650.86370048946, 3176702.3123922977], [359641.4264005116, 3176757.985392296], [359666.7345005057, 3176784.225492301], [359702.97780057625, 3176799.014692297], [359700.0858005235, 3176818.7192922975], [359688.7991005457, 3176852.1781923007], [359687.2997005277, 3176896.1702923034], [359626.685200561, 3176956.983792298], [359611.0450005456, 3176998.0344923], [359612.4513004991, 3177033.4139923053], [359629.58270054124, 3177068.667092306], [359649.46160055976, 3177075.004792305], [359686.41470049205, 3177059.1696923054], [359720.63100051146, 3177059.9355923026], [359742.450500492, 3177072.4693923057], [359765.31670055503, 3177113.929392307], [359818.2002005493, 3177161.534492302], [359880.26410052885, 3177163.135892307], [359910.6384005451, 3177177.4432923044], [359946.34820049384, 3177175.935492311], [360027.8381005201, 3177204.112792311], [360053.1412005484, 3177197.572792308], [360140.54770054424, 3177170.551692307], [360161.72540052584, 3177169.243492309], [360201.13640052476, 3177167.450392304], [360245.4097005649, 3177149.9400923043], [360284.7451005194, 3177087.3571923077], [360301.88000051, 3177050.1937923036], [360319.6270005467, 3177027.4763923013], [360433.6582005497, 3177014.813292308], [360471.8689005027, 3176999.892192306], [360519.3814005202, 3177016.4315923094], [360543.4132005706, 3177055.0221923], [360565.77070051944, 3177122.0361923026], [360614.8393005531, 3177183.7547923103], [360707.60670055926, 3177299.8470923104], [360767.76230056264, 3177350.538792306], [360802.4726005307, 3177397.046592313], [360826.605700531, 3177440.1645923145], [360859.9113005263, 3177465.806192315], [360992.27570050734, 3177545.786292318], [361065.12630054913, 3177532.5613923166], [361179.0588005623, 3177459.2397923134], [361219.4822005307, 3177450.834292317], [361281.41840048396, 3177454.937992312], [361342.91600051336, 3177445.919392309], [361375.4455005351, 3177436.7550923135], [361408.03430051473, 3177436.579992312], [361435.3763004835, 3177420.18439231], [361471.41480052005, 3177389.7143923095], [361495.17830053973, 3177379.391292312], [361553.650600516, 3177309.8795923055], [361594.5584005435, 3177286.3614923116], [361635.488500528, 3177276.3764923094], [361682.3294005515, 3177283.84679231], [361732.73290049215, 3177289.807792313], [361751.2119005437, 3177282.157792314], [361789.24510054535, 3177216.4130923096], [361792.2904004853, 3177194.692592313], [361774.2690005138, 3177166.922092309], [361772.51390049455, 3177108.4395923074], [361781.8894005451, 3177089.640592304], [361809.8394005352, 3177066.570692303], [361827.2239005577, 3177061.3231923045], [361852.7470005371, 3177046.7245923076], [361866.23690050555, 3177048.7698923023], [361867.60420052684, 3177060.4230923015], [361870.75250053965, 3177077.9319923026], [361881.9268005602, 3177103.115292304], [361881.9466004971, 3177121.255292306], [361890.14300050365, 3177133.089092303], [361899.12580050714, 3177128.1196923074], [361921.08040055505, 3177083.715092307], [361942.87560048606, 3177065.4183923006], [361976.0767004837, 3177019.9762923047], [361986.1181004924, 3177025.338492307], [361994.6922005126, 3177075.6447923095], [361989.5788004877, 3177093.046492309], [361994.09080048045, 3177101.890892304], [362043.68100052455, 3177111.7337923083], [362065.30680048524, 3177108.4920923095], [362080.04860053957, 3177114.0479923035], [362104.90960051166, 3177168.0988923106], [362089.15260049026, 3177190.818592309], [362081.18380052515, 3177218.144892306], [362066.2676005318, 3177242.2332923096], [362053.1469005549, 3177309.017392314], [362041.434700535, 3177384.6725923102], [362025.24350051524, 3177398.3313923096], [362026.2951004896, 3177421.7042923127], [362024.5682005394, 3177445.721792311], [362013.0433005066, 3177457.267392312], [361982.8931005348, 3177461.8867923156], [361983.13750055956, 3177473.5255923136], [362000.4207004868, 3177497.949592314], [361998.37190054904, 3177531.225592313], [361992.14860053756, 3177600.6120923203], [362025.3193005644, 3177720.9036923214], [362046.916400549, 3177869.0166923194], [362072.40990048915, 3177906.146592322], [362074.9252004882, 3177999.6283923285], [362087.156600539, 3178009.5846923245], [362094.93290056044, 3178055.792392327], [362131.65870055, 3178166.1370923263], [362168.5835005002, 3178184.928292335], [360646.16200054646, 3179188.402492354], [360896.67270055064, 3179839.5455923663], [359967.9970005136, 3180098.8424923737], [359739.74230049894, 3180162.576592369], [358799.2259005021, 3180306.553192371], [358128.5809005047, 3180409.2188923764], [357996.01770056237, 3181069.9424923896], [357436.22290056455, 3183045.3910924313], [357421.6070005788, 3183137.9686924308], [357381.66670053184, 3183173.5223924313], [357326.1631005686, 3183199.032692438], [357282.628800501, 3183231.4867924405], [357271.28880054713, 3183312.156192436], [357222.17300052673, 3183337.249592439], [357158.0536005174, 3183347.464392442], [357071.7113005171, 3183389.783792446], [357005.83690057014, 3183394.077392437], [356946.0821005724, 3183425.0901924428], [356907.2060005331, 3183452.749592441], [356865.67480050697, 3183481.0203924463], [356837.0644005737, 3183537.9186924454], [356826.8596005454, 3183582.69109244], [356788.4201005597, 3183623.2110924427], [356757.04640054284, 3183654.226392441], [356743.0885005565, 3183715.3063924448], [356701.8958005422, 3183759.1155924452], [356671.33600054495, 3183801.599192453], [356624.83220058086, 3183832.1332924473], [356564.38800050766, 3183894.753792448], [356556.9997005862, 3184010.698492451], [356497.515700547, 3184036.7366924523], [356410.36100056884, 3184117.717092453], [356353.2412005875, 3184144.3306924575], [356268.62400051346, 3184163.139292459], [356204.9345005781, 3184192.914892459], [356163.4695005386, 3184230.837092459], [356048.5982005434, 3184218.9799924544], [356013.3341005895, 3184227.686892452], [355968.40200053237, 3184225.487692458], [355930.8651005742, 3184218.871592458], [355876.8650005534, 3184195.568992458], [355838.2491005737, 3184187.3119924557], [355809.90690058935, 3184187.310292459], [355791.3764005166, 3184189.4896924607], [355769.5783005442, 3184194.9346924555], [355751.04790055915, 3184203.647392458], [352242.9213005366, 3183413.304192436], [352143.4835005293, 3183386.175492437], [351340.61740056763, 3183007.0020924318], [351326.2796005276, 3183002.0874924283], [348042.90780061076, 3182492.028892413], [345819.06180059013, 3182174.927992408], [345313.4168005473, 3183099.6799924253], [343987.39770060696, 3185039.8942924724], [343992.35990062833, 3185658.137192483], [344261.97950063756, 3192369.42079263], [344425.82450058544, 3193826.8115926613], [344224.38020059734, 3201873.3398928344], [343906.99100058695, 3207621.3492929586], [343788.43590058293, 3209769.1828930057], [343731.2887006318, 3213709.3097930877], [344733.68690062035, 3213317.7122930773], [344467.45420061116, 3214620.640793109], [342960.39040057, 3215101.89909312], [342797.00390057976, 3216207.059893138], [342876.2185006424, 3216946.5006931555], [342197.2384005938, 3217926.7207931755], [342142.9956005728, 3218374.2203931846], [342226.8079006121, 3218532.021193185], [342253.9818006027, 3218583.195593188], [342274.81270064035, 3218622.418293187], [343033.0459006325, 3220050.121193225], [343083.40630062483, 3220144.9476932194], [344454.0685006184, 3222725.7999932785], [345047.3716006455, 3223483.9907932947], [345877.4837006327, 3223465.7206932986], [348591.635100569, 3226905.2605933696], [349413.8990005858, 3232479.0144934915], [350397.0182005599, 3239142.669893633], [349261.1204006005, 3239294.500193633], [345835.29040060507, 3239740.961193637], [346281.45550062315, 3245118.0685937507], [347469.9429006368, 3248610.667993831], [345091.92680065124, 3248741.944893834], [344916.82110061834, 3249608.1771938535], [344560.1011006065, 3250894.463593874], [345344.9894006398, 3251449.3804938896], [345338.77990060725, 3251456.9547938895], [345374.7506006096, 3251475.2334938864], [345326.10220063163, 3251497.5913938917], [345292.1626005701, 3251544.6699938937], [345297.2453005676, 3251577.7120938944], [345283.7596005851, 3251597.7666938915], [345259.69530061673, 3251618.002293893], [345245.9451006036, 3251682.633093889], [345249.65920059197, 3251738.8428938994], [345233.72590057313, 3251806.5250938972], [345243.3345006375, 3251857.424993895], [345230.7659005824, 3251962.179593898], [345216.5773006262, 3252056.6225939007], [345202.8826005721, 3252083.1278939033], [345209.65390063904, 3252127.639893901], [345195.16430063, 3252192.9203939023], [345178.14610059874, 3252252.2290939093], [345178.499400613, 3252327.2259939075], [345187.4217006053, 3252421.8597939126], [345182.03430063487, 3252472.2674939106], [345201.4762006206, 3252587.7474939134], [345159.38520060683, 3252726.4852939136], [345120.2373006267, 3252781.684093922], [345097.11640057294, 3252822.8419939196], [345090.02800060064, 3252860.25369392], [345107.39180064306, 3252922.5504939216], [345100.29820058733, 3252958.226393922], [345078.33280058997, 3252989.0281939236], [345107.3251006462, 3253029.856693926], [345107.2003005794, 3253076.788593924], [345030.4320005928, 3253208.530793925], [345019.699700617, 3253285.173793924], [345024.5606006122, 3253334.9580939314], [345020.58340065565, 3253390.8531939243], [345051.841300618, 3253426.9996939315], [345107.8776006472, 3253455.1447939277], [345136.59590058366, 3253480.4248939324], [345133.5686006116, 3253530.02239393], [345138.23020058806, 3253577.0505939336], [345156.20940061973, 3253611.827193931], [345186.71610063786, 3253625.628593932], [345271.20110062923, 3253633.8474939326], [345360.5244005723, 3253712.351693941], [345471.4316005986, 3253795.966493935], [345545.56900060934, 3253858.620693942], [345569.5059005818, 3253938.302493946], [345678.2670006292, 3254051.207093949], [345735.4090006406, 3254074.6646939465], [345795.5400006487, 3254081.455693943], [345858.3064006336, 3254133.0373939476], [345925.1190006309, 3254213.392893941], [345974.32320065063, 3254336.444993946], [346030.91730056854, 3254456.044793957], [346043.56470058765, 3254498.32699395], [346046.7373006455, 3254582.3709939537], [346095.5822005882, 3254755.482993955], [346096.7234005922, 3254814.33959396], [346131.22770060785, 3254958.296093963], [346092.60420058225, 3255021.072893964], [346084.23080061935, 3255105.949093966], [346130.78960061993, 3255152.43879397], [346181.7436005822, 3255187.69389397], [346163.86210057733, 3255262.2657939703], [346172.720100613, 3255342.7654939704], [346212.3899006296, 3255435.755993975], [346249.09730061213, 3255464.057993978], [346243.96350064524, 3255527.2217939734], [346279.13590064377, 3255636.7611939786], [346271.33080064855, 3255691.5960939764], [346291.82110063353, 3255736.8964939765], [346326.0581006094, 3255787.7218939825], [346332.52670059935, 3255851.580493982], [346325.8062006155, 3255888.105093984], [346316.03100065317, 3255953.485593986], [346296.96200057794, 3255971.036993985], [346266.1099005637, 3256038.001893988], [346256.2841005875, 3256070.7825939856], [346260.75440060324, 3256100.6765939835], [346275.06810056895, 3256138.9383939854], [346283.3570005916, 3256191.9207939855], [346257.4770006272, 3256235.6368939904], [346237.03790058685, 3256277.7727939957], [346227.5455005836, 3256355.670093991], [346243.7586005933, 3256439.360893996], [346244.49380057026, 3256520.2704939973], [346256.432000606, 3256578.2431939975], [346220.86290063336, 3256627.7551939986], [346175.48560064833, 3256655.192594003], [346149.2981006124, 3256703.5718940003], [346114.1451005709, 3256750.0902940007], [346107.9156006451, 3256826.080294004], [346076.88070064224, 3256867.792194005], [346047.86810063035, 3256889.828894], [346012.0827005966, 3256910.6511940006], [345988.38440059207, 3256988.3744940083], [345957.034300573, 3257087.3638940137], [345930.1879006129, 3257116.7889940073], [345936.1269006219, 3257150.2463940117], [345917.96050058876, 3257187.0638940097], [345905.71370061394, 3257236.6006940156], [345901.0404006323, 3257279.7783940104], [345882.26250064967, 3257306.6495940113], [345882.08290059894, 3257341.238894015], [345903.48850058723, 3257396.5230940157], [345904.1013006496, 3257425.822294014], [345896.445500607, 3257462.0132940183], [345896.64210059546, 3257517.3581940182], [345897.8154005969, 3257569.6160940174], [345918.5175006018, 3257609.5682940185], [345913.0960006111, 3257651.2907940247], [345897.1125006217, 3257692.3516940195], [345899.74380057835, 3257731.5070940205], [345890.7824005707, 3257754.0978940176], [345893.11360065005, 3257821.764794023], [345855.9216006013, 3257874.716694027], [345864.3072006409, 3257899.122594023], [345880.30220065144, 3257957.045294022], [345947.5248006346, 3257990.4365940248], [345966.7215006424, 3258061.502594026], [345964.89780065103, 3258204.3167940313], [345968.84620057757, 3258234.3431940335], [345952.97000063246, 3258259.809194033], [345965.9556005736, 3258354.886094035], [345960.8723005869, 3258505.59139404], [345968.36750063556, 3258571.119594043], [345978.64940057625, 3258605.373594046], [345974.10410063074, 3258644.4384940406], [345980.8437005805, 3258669.492194037], [345998.2323005692, 3258728.9821940465], [345988.35060059384, 3258765.5747940456], [345994.2577006512, 3258812.051094046], [345970.64290063595, 3258846.5809940416], [345969.46230060665, 3258905.784194043], [345964.04190064454, 3258924.619194046], [345936.4731006469, 3258944.0531940456], [345921.81910059054, 3259002.571194045], [345900.4150005956, 3259042.8016940546], [345904.9758005779, 3259069.5675940537], [345925.93260059546, 3259075.8656940474], [345938.9622006375, 3259117.054194051], [345931.8047006281, 3259128.9342940506], [345911.6882006131, 3259133.457194052], [345900.83540059556, 3259139.061894054], [345895.92450058117, 3259165.5734940516], [345906.7057006236, 3259195.9046940524], [345916.3702005794, 3259214.565994052], [345920.31650065107, 3259237.323494053], [345919.33090065425, 3259267.697594055], [345913.945500609, 3259311.7585940594], [345917.44320057944, 3259363.7886940525], [345906.881100573, 3259382.7171940617], [345951.00740063813, 3259371.1385940593], [345957.04170063045, 3259383.113694056], [345958.1239005957, 3259407.559494054], [346014.66040058644, 3259421.8044940606], [346027.3284005825, 3259440.855094062], [346033.7322006285, 3259460.5285940566], [346044.1514006456, 3259471.8874940593], [346081.87330064306, 3259474.135694057], [346122.77500060527, 3259485.1381940567], [346126.19670064776, 3259529.878194056], [346118.81400060444, 3259566.3048940604], [346094.2030006246, 3259610.338394062], [346036.24730058433, 3259765.3977940683], [345980.5813006181, 3259817.6371940677], [345947.13060062286, 3259885.4407940647], [345904.0602005753, 3259943.201594068], [345879.66460060247, 3259984.7011940647], [345884.87940057827, 3260004.9539940683], [345911.6411006496, 3260043.6051940736], [345952.2025006319, 3260071.4572940716], [346022.0159006235, 3260084.3970940737], [346148.5171006453, 3260139.7000940684], [346151.4338006064, 3260182.834294073], [346170.5466006299, 3260233.8026940753], [346213.3889005857, 3260279.4502940816], [346237.24840058916, 3260332.6262940736], [346255.37970059266, 3260369.8872940773], [346266.0566005842, 3260415.6380940797], [346285.9693005724, 3260479.8945940803], [346307.5031005909, 3260522.371994081], [346288.3626005786, 3260553.3911940847], [346289.09640064044, 3260595.1085940856], [346284.6611005933, 3260639.5244940817], [346257.70240064024, 3260909.776894084], [348997.97650057694, 3261087.7231940953], [349001.4626005605, 3264312.0821941635], [348988.173900623, 3268676.1261942554], [351525.5894005978, 3269203.825394268], [353589.0806005731, 3269580.2290942757], [356287.40570061567, 3271344.224994308], [356328.0721006039, 3271455.7714943113], [356432.5887005356, 3271742.451694319], [356332.50590057916, 3271867.2943943203], [352643.0445006074, 3275629.5145944036], [352604.2744006292, 3275668.9982944047], [345755.3128006254, 3282645.0562945385], [345791.1463006046, 3285955.2650946127], [345833.0700006591, 3291348.4708947274], [346552.5670006371, 3291267.6930947257], [346898.2075006115, 3291242.451794726], [347538.45310063683, 3291191.3901947285], [347633.49090060894, 3291154.044694726], [347710.7582006501, 3291135.3473947183], [347870.402500643, 3291113.0426947246], [348233.1411006341, 3291100.068094724], [348664.7179006317, 3291085.5036947215], [349400.10360064544, 3291059.5452947235], [349697.64890058094, 3290971.253294717], [350115.36460062664, 3290959.7007947224], [350507.60420058266, 3290956.9412947227], [350690.50830062793, 3290945.53019472], [352378.80360056483, 3290915.355894717], [352854.3946005647, 3290897.3505947194], [353138.62240057415, 3290898.976994718], [353737.2849006304, 3290890.1964947134], [353635.1163006078, 3289248.52469468], [353286.6780005633, 3288435.273594665], [354189.97780058696, 3287849.0662946515], [352885.52090061584, 3286879.522594638], [352879.26780057454, 3286321.1482946277], [352915.81570063607, 3286287.3606946226], [352988.75760059274, 3286290.1260946197], [353060.7768005617, 3286306.4167946237], [353215.6206005494, 3286324.591494621], [353339.4355006207, 3286347.6086946256], [353507.635000584, 3286381.564494628], [353611.14270060137, 3286413.9461946283], [353690.4450006187, 3286419.679994627], [353711.7126005756, 3286409.7840946275], [353772.3489005546, 3286372.9486946287], [353805.0197006039, 3286334.071894626], [353869.1770006026, 3286152.92729462], [353903.3854005748, 3285862.0011946172], [353935.2012005948, 3285607.219794612], [353927.6356005629, 3285472.633894603], [354023.31660061586, 3285431.058894611], [354084.0956005986, 3285425.014394606], [354129.09920058097, 3285392.736894605], [354152.4396005693, 3285349.4616946033], [354159.63510062813, 3285312.316994607], [354146.20220059407, 3285255.981794601], [354131.7174005507, 3285214.660494606], [354131.27140058944, 3285192.993494604], [354168.8179005643, 3285164.645194601], [354311.2664005548, 3284987.981994595], [354354.10620055714, 3284874.476094592], [354356.0373005491, 3284806.970794596], [354341.8227005609, 3284735.8128945916], [354412.8971006261, 3284690.591494589], [354461.88560057594, 3284639.7976945853], [354529.7426006145, 3284594.914994587], [354600.32450062316, 3284512.628294584], [354727.46270058176, 3284460.572594583], [354821.73240062443, 3284439.2140945834], [354858.3386006056, 3284379.372994583], [354922.4383005452, 3284333.584994585], [354951.83620056574, 3284289.175794582], [354979.79490058456, 3284195.886894583], [355022.6485005977, 3283995.369494581], [355103.32380056253, 3283900.458494573], [355242.93750061793, 3283825.232794574], [355353.85380056174, 3283768.2835945734], [355389.80760062113, 3283716.508794574], [355517.79070060316, 3283699.9351945645], [355615.91660061025, 3283761.524694573], [355706.6120005684, 3283749.9985945732], [355835.4284006021, 3283739.595994566], [355887.756200574, 3283730.615994568], [355892.82470062224, 3283691.696894564], [355923.3257005967, 3283676.0082945717], [355987.5634006228, 3283671.9331945707], [356114.08380055707, 3283659.341194571], [356216.62240059604, 3283715.1552945725], [356300.0433005797, 3283977.4999945746], [356334.67000054906, 3284094.314494578], [356075.0750005544, 3284373.5822945805], [356126.60550053767, 3284765.560294598], [355486.16800057126, 3285436.8348946073], [354363.00990056724, 3286935.3358946396], [354389.1238005933, 3286953.290094635], [357019.37510058936, 3288839.003694679], [357340.1092005379, 3288982.1327946847], [357379.76750058413, 3289000.093694683], [357793.1176006098, 3289182.9113946795], [358298.6766005793, 3289403.6437946875], [358046.7632005305, 3289687.224794698], [357450.31220055104, 3290371.9093947075], [357732.4092005829, 3290580.632694714], [358066.41000053287, 3290835.713594719], [359728.3259005518, 3290814.3061947166], [360502.8263005917, 3290802.29899472], [363040.3021005922, 3290772.482494719], [366941.93690053973, 3290723.3795947223], [367392.9022005362, 3289052.479894688], [367407.6067005297, 3288998.254394685], [367444.20570055675, 3288864.9839946805], [367464.81290056783, 3288792.3952946803], [367528.60520052677, 3288608.3550946782], [367633.9675005168, 3288313.8591946666], [367743.9122005145, 3288002.944394667], [367839.5948005257, 3287730.5121946554], [369543.7775005561, 3287707.3280946575], [370332.7923005584, 3287701.7020946583], [370970.6438005403, 3287698.868394656], [371412.7476004789, 3287689.076294654], [371683.8865004888, 3287689.7358946586], [372449.32000052143, 3287674.3809946533], [373042.2379005016, 3287661.4120946587], [377427.64900047344, 3287607.410294658], [377418.235600535, 3287901.062494665], [376868.27320052206, 3288603.823794681], [376643.0721005062, 3288880.458794685], [376424.00090048235, 3289372.002794697], [375498.5268005393, 3290888.3289947254], [374878.746000477, 3291144.3982947306], [374814.10340047075, 3291172.2989947307], [374235.98270050535, 3291421.824994732], [373733.63960054464, 3291835.3729947405], [375067.8508004791, 3293923.9267947944], [376578.61110050994, 3293352.7833947768], [376509.07610053394, 3293831.3965947917], [376480.19280048524, 3294208.3486947976], [376639.5709005177, 3294343.729194795], [376770.61880049366, 3294442.7571947947], [377127.4443004728, 3294671.486594804], [377264.38170052663, 3294749.7839948037], [377366.0946005012, 3294751.2616948094], [377463.7993004956, 3294747.4134948035], [377559.2995004823, 3294767.424594807], [377705.6705004804, 3294821.9721948127], [377837.7596005212, 3294876.1682948084], [377915.8443004776, 3294907.691394808], [377986.4792004895, 3294943.2996948063], [378138.43230050406, 3294925.8654948142], [378194.76450052613, 3294887.7290948085], [378250.77380046505, 3294864.1553948075], [378300.91810047516, 3294867.658794807], [378376.8222004584, 3294859.7429948137], [378428.6827004964, 3294837.3635948086], [378492.89440050896, 3294779.718594807], [378533.9588004996, 3294763.932294805], [378668.15940048214, 3294769.3382948115], [378732.78140046296, 3294801.9875948094], [378809.27130051603, 3294860.99809481], [378889.05300045933, 3294937.3095948147], [378956.8588004915, 3294967.3564948156], [379071.04920047935, 3295065.424094813], [379124.40240051126, 3295125.2406948116], [379259.5473004818, 3295242.949294815], [379332.32000046154, 3295305.7262948174], [379415.4347005119, 3295394.599894814], [379498.6309004561, 3295457.4136948194], [379548.05540049763, 3295486.238494823], [379675.40730047977, 3295596.10179483], [381010.5544004806, 3295344.9501948184]]]	\N	\N
\.


--
-- Data for Name: municipality_map_layer_base; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.municipality_map_layer_base (id, map_layer_id, municipality_id) FROM stdin;
\.


--
-- Data for Name: municipality_signatures; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.municipality_signatures (id, signer_name, department, orden, municipality_id, created_at, updated_at, signature) FROM stdin;
\.


--
-- Data for Name: national_id; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.national_id (id, national_id_number, national_id_type, user_id) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notifications (id, user_id, applicant_email, comment, file, creation_date, seen_date, dependency_file, notified, notifying_department, notification_type, resolution_id, created_at, updated_at, folio) FROM stdin;
\.


--
-- Data for Name: password_recoveries; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.password_recoveries (id, email, token, expiration_date, created_at, updated_at, used) FROM stdin;
1	test_user_1@example.com	0933953c-82b3-4ce3-8184-fe9faf96b80c	2025-06-01 16:55:23.18156	2025-05-31 16:55:23.181777	2025-05-31 16:55:23.181789	0
2	test_user_2@example.com	de5c5eab-bab7-4d76-bcee-f2799654be90	2025-06-01 16:55:23.181862	2025-05-31 16:55:23.181865	2025-05-31 16:55:23.181866	0
3	test_user_3@example.com	a28ac2b5-fb19-4a68-96fb-014f6370e9aa	2025-06-01 16:55:23.181896	2025-05-31 16:55:23.181898	2025-05-31 16:55:23.181899	0
4	test_user_4@example.com	a01dbc67-ef2f-4370-ab2e-eea2ccc70fdd	2025-06-01 16:55:23.181919	2025-05-31 16:55:23.18192	2025-05-31 16:55:23.181921	0
5	test_user_5@example.com	7c3b8fa9-1a8f-4ad6-a217-94ee086d6dd3	2025-06-01 16:55:23.181937	2025-05-31 16:55:23.181939	2025-05-31 16:55:23.181939	0
6	test_user_1@example.com	d4032030-3d30-4d33-9edc-16f0dc162160	2025-06-01 16:55:23.181955	2025-05-31 16:55:23.181957	2025-05-31 16:55:23.181957	0
7	test_user_2@example.com	b0619425-a9a4-45c7-93c9-85ac3940af36	2025-06-01 16:55:23.181971	2025-05-31 16:55:23.181973	2025-05-31 16:55:23.181973	0
8	test_user_3@example.com	fa931399-8d46-48f1-b83d-914874f1e64e	2025-06-01 16:55:23.181986	2025-05-31 16:55:23.181988	2025-05-31 16:55:23.181988	0
9	test_user_4@example.com	ea883138-09b7-4dba-bdb9-e1f3bbde785c	2025-06-01 16:55:23.182001	2025-05-31 16:55:23.182002	2025-05-31 16:55:23.182003	0
10	test_user_5@example.com	453c2374-3186-46d4-948c-d29f730aa748	2025-06-01 16:55:23.182015	2025-05-31 16:55:23.182016	2025-05-31 16:55:23.182017	0
11	test_user_1@example.com	d2cb4f7e-cd00-4411-95f3-6c17eac5f8d3	2025-06-01 16:55:23.189504	2025-05-31 16:53:23.18952	2025-05-31 16:53:23.189527	0
12	test_user_2@example.com	7194367c-c123-4da3-8bdd-06fcdc46f69f	2025-06-01 16:55:23.189569	2025-05-31 16:52:23.189571	2025-05-31 16:52:23.189573	0
17	niux.legend@gmail.com	ad92992a-a58d-48f3-a06d-5c1c9d32872e	2025-06-01 17:58:50.367864	2025-05-31 17:58:50.367873	2025-05-31 13:58:50.364194	0
\.


--
-- Data for Name: permit_renewals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.permit_renewals (id, created_at, updated_at, id_consulta_requisitos, id_tramite) FROM stdin;
\.


--
-- Data for Name: procedure_registrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.procedure_registrations (id, reference, area, business_sector, municipality_id, geom, procedure_type, procedure_origin, bbox, historical_id) FROM stdin;
6	REF-001	120.5	Retail	1	\N	New License	Online	\N	\N
7	REF-002	250.75	Restaurant	1	0103000020657F000001000000050000009D62140FC1A61741192A6E5F47194841214F784C77D81841A23757AEF1184841E6CFE4FC37DB184143D3F01339444841A8BE912B16AA17410047C4278F4448419D62140FC1A61741192A6E5F47194841	Renewal	Counter	-106.15,28.55,-105.95,28.75	\N
8	REF-003	85	Services	2	\N	Permit	Online	\N	\N
9	REF-004	300	Industrial	1	0103000020657F00000100000005000000DDEA73FAD8121841C29E6D5C4D28484159A5330B663118418405639D4428484139F001A0B431184101815592982C484195E4FB0A2913184119F66152A12C4841DDEA73FAD8121841C29E6D5C4D284841	New License	Counter	-106.08,28.62,-106.06,28.64	\N
10	REF-005	175	Office	2	\N	Modification	Online	\N	\N
11	REF-006	50.25	Retail	3	\N	New License	Counter	\N	\N
12	REF-API-1	123.45	Test	1	\N	API	Script	\N	\N
13	REF-API-1	321	GeomSector	2	\N	API	Script	\N	\N
14	REF-API-1	321	GeomSector	2	\N	API	Script	\N	\N
\.


--
-- Data for Name: procedures; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.procedures (id, folio, current_step, user_signature, user_id, window_user_id, entry_role, documents_submission_date, procedure_start_date, window_seen_date, license_delivered_date, has_signature, no_signature_date, official_applicant_name, responsibility_letter, sent_to_reviewers, sent_to_reviewers_date, license_pdf, payment_order, status, step_one, step_two, step_three, step_four, director_approval, created_at, updated_at, window_license_generated, procedure_type, license_status, reason, renewed_folio, requirements_query_id) FROM stdin;
3	string	0	string	\N	\N	0	2025-03-17 14:22:12.079	2025-03-17 14:22:12.079	2025-03-17 14:22:12.079	2025-03-17 14:22:12.079	0	2025-03-17 14:22:12.079	string	string	0	2025-03-17 14:22:12.079	string	string	0	0	0	0	0	0	2025-03-17 10:28:44.215077	2025-03-17 10:28:44.215077	0	string	string	string	string	\N
1	PROC-001	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	\N	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	\N	Commercial License	\N	\N	\N	\N
2	PROC-002	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	\N	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	\N	Industrial License	\N	\N	\N	\N
4	PROC-004	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	\N	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	\N	Food Service License	\N	\N	\N	\N
5	PROC-005	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	\N	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	\N	Automotive Service	\N	\N	\N	\N
28	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	\N	\N	\N	\N	licencia_construccion	en_proceso	\N	\N	\N
29	TEST-002	4	user_signature_data_2	2	3	1	2025-03-02 15:58:23.030997	2025-03-03 15:58:23.030997	2025-03-07 15:58:23.030997	2025-05-01 15:58:23.030997	1	\N	María González	\N	\N	\N	\N	/uploads/payment_orders/order_test_002.pdf	2	\N	\N	\N	\N	\N	\N	\N	\N	licencia_comercial	completado	\N	\N	\N
31	TEST-004	2	user_signature_data_4	3	4	1	2025-04-16 15:58:23.030997	2025-04-17 15:58:23.030997	2025-04-21 15:58:23.030997	\N	1	\N	Carlos Rodríguez	\N	\N	\N	\N	/uploads/payment_orders/order_test_004.pdf	3	\N	\N	\N	\N	\N	\N	\N	\N	licencia_construccion	rechazado	\N	\N	\N
30	TEST-003	3	user_signature_data_3	2	3	1	2025-05-16 15:58:23.030997	2025-05-17 15:58:23.030997	2025-05-19 15:58:23.030997	\N	1	\N	María González	\N	\N	\N	\N	/uploads/payment_orders/order_test_003.pdf	1	\N	\N	\N	\N	\N	\N	\N	\N	refrendo	en_proceso	\N	TEST-002	\N
32	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 15:58:38.626959	2025-05-31 15:58:38.626959	0	licencia_construccion	en_proceso	\N	\N	\N
33	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 15:58:38.679951	2025-05-31 15:58:38.679951	0	licencia_construccion	en_proceso	\N	\N	\N
34	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 15:58:38.695132	2025-05-31 15:58:38.695132	0	refrendo	en_proceso	\N	TEST-002	\N
35	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:01:02.282288	2025-05-31 16:01:02.282288	0	licencia_construccion	en_proceso	\N	\N	\N
36	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:01:02.342077	2025-05-31 16:01:02.342077	0	licencia_construccion	en_proceso	\N	\N	\N
37	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:01:02.359781	2025-05-31 16:01:02.359781	0	refrendo	en_proceso	\N	TEST-002	\N
38	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:03:44.238438	2025-05-31 16:03:44.238438	0	licencia_construccion	en_proceso	\N	\N	\N
39	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:03:44.297307	2025-05-31 16:03:44.297307	0	licencia_construccion	en_proceso	\N	\N	\N
40	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:03:44.315223	2025-05-31 16:03:44.315223	0	refrendo	en_proceso	\N	TEST-002	\N
41	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:04:43.60891	2025-05-31 16:04:43.60891	0	licencia_construccion	en_proceso	\N	\N	\N
42	HIST-001	4	user_signature_data_hist_1	1	2	1	2023-05-31 15:58:23.030997	2023-05-31 15:58:23.030997	2023-06-05 15:58:23.030997	2023-06-30 15:58:23.030997	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	2	\N	\N	\N	\N	0	2025-05-31 16:04:43.620887	2025-05-31 16:04:43.620887	0	licencia_construccion	completado	\N	\N	\N
43	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:08:16.854935	2025-05-31 16:08:16.854935	0	licencia_construccion	en_proceso	\N	\N	\N
44	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:08:16.903359	2025-05-31 16:08:16.903359	0	licencia_construccion	en_proceso	\N	\N	\N
45	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:08:16.920779	2025-05-31 16:08:16.920779	0	refrendo	en_proceso	\N	TEST-002	\N
46	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:09:41.999288	2025-05-31 16:09:41.999288	0	licencia_construccion	en_proceso	\N	\N	\N
47	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:09:42.055368	2025-05-31 16:09:42.055368	0	licencia_construccion	en_proceso	\N	\N	\N
48	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:09:42.072894	2025-05-31 16:09:42.072894	0	refrendo	en_proceso	\N	TEST-002	\N
49	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:10:38.696283	2025-05-31 16:10:38.696283	0	licencia_construccion	en_proceso	\N	\N	\N
50	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:10:38.754632	2025-05-31 16:10:38.754632	0	licencia_construccion	en_proceso	\N	\N	\N
51	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:10:38.771091	2025-05-31 16:10:38.771091	0	refrendo	en_proceso	\N	TEST-002	\N
52	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:11:15.971512	2025-05-31 16:11:15.971512	0	licencia_construccion	en_proceso	\N	\N	\N
53	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:11:16.016596	2025-05-31 16:11:16.016596	0	licencia_construccion	en_proceso	\N	\N	\N
54	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:11:16.032181	2025-05-31 16:11:16.032181	0	refrendo	en_proceso	\N	TEST-002	\N
55	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:12:04.700984	2025-05-31 16:12:04.700984	0	licencia_construccion	en_proceso	\N	\N	\N
56	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:12:04.75088	2025-05-31 16:12:04.75088	0	licencia_construccion	en_proceso	\N	\N	\N
57	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:12:04.766927	2025-05-31 16:12:04.766927	0	refrendo	en_proceso	\N	TEST-002	\N
58	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:13:52.310374	2025-05-31 16:13:52.310374	0	licencia_construccion	en_proceso	\N	\N	\N
59	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:13:52.361054	2025-05-31 16:13:52.361054	0	licencia_construccion	en_proceso	\N	\N	\N
60	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:13:52.377568	2025-05-31 16:13:52.377568	0	refrendo	en_proceso	\N	TEST-002	\N
61	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:19:07.765264	2025-05-31 16:19:07.765264	0	licencia_construccion	en_proceso	\N	\N	\N
62	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:19:07.810399	2025-05-31 16:19:07.810399	0	licencia_construccion	en_proceso	\N	\N	\N
63	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:19:07.826169	2025-05-31 16:19:07.826169	0	refrendo	en_proceso	\N	TEST-002	\N
64	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:19:42.012032	2025-05-31 16:19:42.012032	0	licencia_construccion	en_proceso	\N	\N	\N
65	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:19:42.057396	2025-05-31 16:19:42.057396	0	licencia_construccion	en_proceso	\N	\N	\N
66	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:19:42.075905	2025-05-31 16:19:42.075905	0	refrendo	en_proceso	\N	TEST-002	\N
67	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:20:11.815037	2025-05-31 16:20:11.815037	0	licencia_construccion	en_proceso	\N	\N	\N
68	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:20:11.861694	2025-05-31 16:20:11.861694	0	licencia_construccion	en_proceso	\N	\N	\N
69	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:20:11.878498	2025-05-31 16:20:11.878498	0	refrendo	en_proceso	\N	TEST-002	\N
70	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:20:40.709097	2025-05-31 16:20:40.709097	0	licencia_construccion	en_proceso	\N	\N	\N
71	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:20:40.759987	2025-05-31 16:20:40.759987	0	licencia_construccion	en_proceso	\N	\N	\N
72	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:20:40.777906	2025-05-31 16:20:40.777906	0	refrendo	en_proceso	\N	TEST-002	\N
73	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:21:31.9021	2025-05-31 16:21:31.9021	0	licencia_construccion	en_proceso	\N	\N	\N
74	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:21:31.949175	2025-05-31 16:21:31.949175	0	licencia_construccion	en_proceso	\N	\N	\N
75	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:21:31.964468	2025-05-31 16:21:31.964468	0	refrendo	en_proceso	\N	TEST-002	\N
76	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:21:56.663206	2025-05-31 16:21:56.663206	0	licencia_construccion	en_proceso	\N	\N	\N
77	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:21:56.713258	2025-05-31 16:21:56.713258	0	licencia_construccion	en_proceso	\N	\N	\N
78	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:21:56.730046	2025-05-31 16:21:56.730046	0	refrendo	en_proceso	\N	TEST-002	\N
79	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:24:23.340338	2025-05-31 16:24:23.340338	0	licencia_construccion	en_proceso	\N	\N	\N
80	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:24:23.404975	2025-05-31 16:24:23.404975	0	licencia_construccion	en_proceso	\N	\N	\N
81	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:24:23.420664	2025-05-31 16:24:23.420664	0	refrendo	en_proceso	\N	TEST-002	\N
82	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:25:23.09023	2025-05-31 16:25:23.09023	0	licencia_construccion	en_proceso	\N	\N	\N
83	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:25:23.166088	2025-05-31 16:25:23.166088	0	licencia_construccion	en_proceso	\N	\N	\N
84	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:25:23.18156	2025-05-31 16:25:23.18156	0	refrendo	en_proceso	\N	TEST-002	\N
85	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:26:22.706439	2025-05-31 16:26:22.706439	0	licencia_construccion	en_proceso	\N	\N	\N
86	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:26:22.758909	2025-05-31 16:26:22.758909	0	licencia_construccion	en_proceso	\N	\N	\N
87	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:26:22.775073	2025-05-31 16:26:22.775073	0	refrendo	en_proceso	\N	TEST-002	\N
88	COPY-39845408	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:30:56.510465	2025-05-31 16:30:56.510465	0	licencia_construccion	en_proceso	\N	\N	\N
89	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:30:56.576093	2025-05-31 16:30:56.576093	0	licencia_construccion	en_proceso	\N	\N	\N
90	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:30:56.591834	2025-05-31 16:30:56.591834	0	refrendo	en_proceso	\N	TEST-002	\N
91	COPY-AEE040A6	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:31:53.168978	2025-05-31 16:31:53.168978	0	licencia_construccion	en_proceso	\N	\N	\N
92	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:31:53.235437	2025-05-31 16:31:53.235437	0	licencia_construccion	en_proceso	\N	\N	\N
93	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:31:53.251574	2025-05-31 16:31:53.251574	0	refrendo	en_proceso	\N	TEST-002	\N
94	COPY-342E68EE	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:34:11.73856	2025-05-31 16:34:11.73856	0	licencia_construccion	en_proceso	\N	\N	\N
95	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:34:11.810971	2025-05-31 16:34:11.810971	0	licencia_construccion	en_proceso	\N	\N	\N
96	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:34:11.828571	2025-05-31 16:34:11.828571	0	refrendo	en_proceso	\N	TEST-002	\N
97	COPY-530709FD	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:35:20.401541	2025-05-31 16:35:20.401541	0	licencia_construccion	en_proceso	\N	\N	\N
98	COPY-7D111353	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:38:10.382735	2025-05-31 16:38:10.382735	0	licencia_construccion	en_proceso	\N	\N	\N
99	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:38:10.450795	2025-05-31 16:38:10.450795	0	licencia_construccion	en_proceso	\N	\N	\N
100	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:38:10.467022	2025-05-31 16:38:10.467022	0	refrendo	en_proceso	\N	TEST-002	\N
101	COPY-E849FB2C	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:40:25.341925	2025-05-31 16:40:25.341925	0	licencia_construccion	en_proceso	\N	\N	\N
102	HIST-F4D8ED60	1	user_signature_data_hist_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	1	0	0	0	0	0	2025-05-31 16:40:25.39448	2025-05-31 16:40:25.39448	0	licencia_construccion	completado	\N	\N	\N
103	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:40:25.420654	2025-05-31 16:40:25.420654	0	licencia_construccion	en_proceso	\N	\N	\N
104	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:40:25.440047	2025-05-31 16:40:25.440047	0	refrendo	en_proceso	\N	TEST-002	\N
105	COPY-402CD452	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:42:47.405448	2025-05-31 16:42:47.405448	0	licencia_construccion	en_proceso	\N	\N	\N
106	HIST-9A337869	1	user_signature_data_hist_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	1	0	0	0	0	0	2025-05-31 16:42:47.443285	2025-05-31 16:42:47.443285	0	licencia_construccion	completado	\N	\N	\N
107	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:42:47.464721	2025-05-31 16:42:47.464721	0	licencia_construccion	en_proceso	\N	\N	\N
108	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:42:47.480672	2025-05-31 16:42:47.480672	0	refrendo	en_proceso	\N	TEST-002	\N
109	COPY-6A87D003	1	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:43:43.979801	2025-05-31 16:43:43.979801	0	licencia_construccion	en_proceso	\N	\N	\N
110	TEST-001	2	user_signature_data_1	1	2	1	2025-05-01 15:58:23.030997	2025-05-02 15:58:23.030997	2025-05-03 15:58:23.030997	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	\N	\N	\N	\N	0	2025-05-31 16:45:11.527492	2025-05-31 16:45:11.527492	0	licencia_construccion	en_proceso	\N	\N	\N
111	COPY-171FA732	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:45:57.399188	2025-05-31 16:45:57.399188	0	licencia_construccion	en_proceso	\N	\N	\N
112	HIST-BFE4B1B1	1	user_signature_data_hist_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	1	0	0	0	0	0	2025-05-31 16:45:57.443441	2025-05-31 16:45:57.443441	0	licencia_construccion	completado	\N	\N	\N
113	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:45:57.465533	2025-05-31 16:45:57.465533	0	licencia_construccion	en_proceso	\N	\N	\N
114	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:45:57.481609	2025-05-31 16:45:57.481609	0	refrendo	en_proceso	\N	TEST-002	\N
115	COPY-9D9A68BB	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:48:50.852398	2025-05-31 16:48:50.852398	0	licencia_construccion	en_proceso	\N	\N	\N
116	HIST-E8D480A3	1	user_signature_data_hist_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	1	0	0	0	0	0	2025-05-31 16:48:50.897298	2025-05-31 16:48:50.897298	0	licencia_construccion	completado	\N	\N	\N
117	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:48:50.920606	2025-05-31 16:48:50.920606	0	licencia_construccion	en_proceso	\N	\N	\N
118	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:48:50.939378	2025-05-31 16:48:50.939378	0	refrendo	en_proceso	\N	TEST-002	\N
119	COPY-4DE35804	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:49:03.295524	2025-05-31 16:49:03.295524	0	licencia_construccion	en_proceso	\N	\N	\N
120	COPY-7EAD652B	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:50:42.925001	2025-05-31 16:50:42.925001	0	licencia_construccion	en_proceso	\N	\N	\N
121	COPY-12C091A1	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:50:56.439766	2025-05-31 16:50:56.439766	0	licencia_construccion	en_proceso	\N	\N	\N
122	COPY-F99387CE	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:54:00.476551	2025-05-31 16:54:00.476551	0	licencia_construccion	en_proceso	\N	\N	\N
123	COPY-5B04169C	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 16:54:09.081582	2025-05-31 16:54:09.081582	0	licencia_construccion	en_proceso	\N	\N	\N
124	HIST-3C9DAED8	1	user_signature_data_hist_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	1	0	0	0	0	0	2025-05-31 16:54:09.114061	2025-05-31 16:54:09.114061	0	licencia_construccion	completado	\N	\N	\N
125	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:54:09.134611	2025-05-31 16:54:09.134611	0	licencia_construccion	en_proceso	\N	\N	\N
126	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 16:54:09.150381	2025-05-31 16:54:09.150381	0	refrendo	en_proceso	\N	TEST-002	\N
127	COPY-3604BCAC	1	user_signature_data_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_test_001.pdf	1	0	0	0	0	0	2025-05-31 17:18:24.901513	2025-05-31 17:18:24.901513	0	licencia_construccion	en_proceso	\N	\N	\N
128	HIST-C15D1FCF	1	user_signature_data_hist_1	1	2	1	\N	\N	\N	\N	1	\N	Juan Pérez	\N	\N	\N	\N	/uploads/payment_orders/order_hist_001.pdf	1	0	0	0	0	0	2025-05-31 17:18:24.939384	2025-05-31 17:18:24.939384	0	licencia_construccion	completado	\N	\N	\N
129	TEST-NEW-001	\N	\N	1	2	1	\N	\N	\N	\N	\N	\N	New Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 17:18:24.959857	2025-05-31 17:18:24.959857	0	licencia_construccion	en_proceso	\N	\N	\N
130	TEST-NEW-002	\N	\N	2	3	1	\N	\N	\N	\N	\N	\N	Renewal Test User	\N	\N	\N	\N	\N	1	\N	\N	\N	\N	0	2025-05-31 17:18:24.974661	2025-05-31 17:18:24.974661	0	refrendo	en_proceso	\N	TEST-002	\N
\.


--
-- Data for Name: provisional_openings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.provisional_openings (id, folio, procedure_id, counter, granted_by_user_id, granted_role, start_date, end_date, status, created_at, updated_at, municipality_id, created_by) FROM stdin;
2	AOD-002-2024	1	1002	2	1	2024-12-05 09:00:00	2025-02-05 17:00:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	1	2
3	AOD-003-2024	5	2001	3	1	2024-12-10 07:30:00	2025-02-10 18:30:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	2	3
4	AOD-004-2024	3	1003	1	1	2024-10-01 08:00:00	2024-11-30 20:00:00	0	2024-10-01 10:15:00	2024-11-30 20:00:00	1	1
5	AOD-005-2024	3	2002	4	1	2024-12-15 09:00:00	2025-01-15 19:00:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	2	4
6	AOD-006-2024	1	3001	5	1	2024-12-20 06:00:00	2025-03-20 22:00:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	3	5
7	AOD-007-2024	1	1004	2	1	2024-11-15 18:00:00	2025-01-15 02:00:00	2	2024-11-15 20:30:00	2025-05-29 11:18:33.667442	1	2
8	AOD-008-2024	1	2003	3	1	2024-12-22 08:30:00	2025-04-22 19:30:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	2	3
9	AOD-009-2024	4	3002	5	1	2024-11-01 05:00:00	2024-12-31 21:00:00	3	2024-11-01 08:45:00	2024-12-01 14:20:00	3	5
10	AOD-010-2024	1	1005	1	1	2024-12-25 10:00:00	2025-05-25 20:00:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	1	1
11	AOD-011-2024	3	2004	4	1	2024-12-28 07:00:00	2025-03-28 19:00:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	2	4
12	AOD-012-2024	3	3003	5	1	2024-09-15 06:00:00	2024-12-15 22:00:00	0	2024-09-15 11:30:00	2024-12-15 22:00:00	3	5
13	AOD-013-2024	3	1006	2	1	2025-01-01 08:00:00	2025-06-01 20:00:00	4	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	1	2
14	AOD-014-2024	2	2005	3	1	2024-12-01 07:00:00	2025-12-01 18:00:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	2	3
15	AOD-015-2024	1	3004	5	1	2024-12-30 09:00:00	2025-03-30 18:00:00	1	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	3	5
16	TEST-2024	1	9999	1	1	2025-05-29 08:00:00	2025-08-27 18:00:00	1	2025-05-29 11:34:58.196336	2025-05-29 11:34:58.19634	1	1
1	AOD-001-2024	1	1001	1	1	2024-12-01 08:00:00	2025-09-26 20:00:00	0	2025-05-29 11:18:33.667442	2025-05-29 11:34:58.263201	1	1
\.


--
-- Data for Name: public_space_mapping; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.public_space_mapping (id, name, space_type, geom) FROM stdin;
\.


--
-- Data for Name: renewal_file_histories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.renewal_file_histories (id, renewal_id, file_name, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: renewal_files; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.renewal_files (id, file, description, renewal_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: renewals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.renewals (id, license_id, renewal_date, status, observations, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: requirements; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.requirements (id, created_at, updated_at, municipality_id, field_id, requirement_code) FROM stdin;
\.


--
-- Data for Name: requirements_querys; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.requirements_querys (id, folio, street, neighborhood, municipality_name, municipality_id, scian_code, scian_name, property_area, activity_area, applicant_name, applicant_character, person_type, minimap_url, restrictions, status, user_id, created_at, updated_at, year_folio, alcohol_sales, primary_folio) FROM stdin;
2	TEST-RQ-001	Av. Principal 123	Centro	Test Municipality	1	722513	Restaurantes con servicio	150.50	120.00	Juan Pérez García	\N	\N	\N	\N	1	1	\N	\N	2024	0	\N
3	TEST-RQ-002	Calle Comercio 456	Industrial	Test Municipality	1	465211	Comercio al por menor	250.75	200.00	María López Rodríguez	\N	\N	\N	\N	1	1	\N	\N	2024	0	\N
4	TEST-RQ-003	Boulevard Norte 789	Residencial	Test Municipality	1	811219	Otros servicios de limpieza	100.25	80.00	Carlos Martínez Silva	\N	\N	\N	\N	1	1	\N	\N	2024	0	\N
5	TEST-RQ-004	Av. Turística 321	Zona Turística	Test Municipality	1	722412	Centros nocturnos, bares	300.00	250.00	Ana Fernández Torres	\N	\N	\N	\N	1	1	\N	\N	2024	0	\N
\.


--
-- Data for Name: reviewers_chat; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reviewers_chat (id, id_tramite, ir_usuario, rol, comentario, imagen, archivo_adjunto, deleted_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: sub_roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sub_roles (id, name, description, municipality_id, deleted_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: technical_sheet_downloads; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.technical_sheet_downloads (id, city, email, age, name, sector, uses, created_at, updated_at, municipality_id, address) FROM stdin;
1	Guadalajara	usuario@ejemplo.com	35	Luis	Residencial	["habitacional", "comercial"]	2025-04-24 09:58:02.366982	2025-04-24 09:58:02.366982	1	Calle Real #123
2	Test City 1	test1@example.com	25-35	John Doe	Commercial	Restaurant operations	2024-01-15 10:00:00	2024-01-15 10:00:00	1	123 Main St
3	Test City 2	test2@example.com	35-45	Jane Smith	Industrial	Manufacturing	2024-01-16 11:00:00	2024-01-16 11:00:00	2	456 Industrial Blvd
4	Test City 3	test3@example.com	45-55	Bob Johnson	Residential	Housing development	2024-01-17 12:00:00	2024-01-17 12:00:00	3	789 Residential Ave
5	Test City 4	test4@example.com	25-35	Alice Brown	Commercial	Retail store	2024-01-18 13:00:00	2024-01-18 13:00:00	19	321 Commerce St
6	Test City 5	test5@example.com	35-45	Charlie Wilson	Mixed	Office and retail complex	2024-01-19 14:00:00	2024-01-19 14:00:00	2	654 Mixed Use Rd
\.


--
-- Data for Name: technical_sheets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.technical_sheets (id, uuid, address, square_meters, coordinates, image, municipality_id, created_at, updated_at, technical_sheet_download_id) FROM stdin;
1	uuid-001	Main Street 123	100	POINT(19.4326 -99.1332)	image1.jpg	1	2023-10-01 12:00:00	2023-10-01 12:00:00	\N
2	uuid-002	Elm Street 456	150	POINT(18.4861 -69.9312)	image2.jpg	1	2023-10-01 14:00:00	2023-10-01 14:00:00	\N
3	uuid-003	Sunset Blvd 789	200	POINT(20.6597 -103.3496)	image3.jpg	1	2023-10-02 09:30:00	2023-10-02 09:30:00	\N
4	uuid-004	5th Avenue 101	120	POINT(34.0522 -118.2437)	image4.jpg	1	2024-01-15 08:00:00	2024-01-15 08:00:00	\N
5	uuid-005	Broadway 202	90	POINT(40.7128 -74.0060)	image5.jpg	1	2024-01-15 10:15:00	2024-01-15 10:15:00	\N
6	uuid-000	Old Road 999	50	POINT(0 0)	old.jpg	1	2021-01-01 00:00:00	2021-01-01 00:00:00	\N
8	6dffcc78-8549-4ed0-9a5b-40a75c6036d4	Av. Central #45	120	20.6751,-103.3476	https://example.com/image.jpg	2	2025-04-24 09:59:55.314739	2025-04-24 09:59:55.314739	1
9	00000000-0000-0000-0000-000000000001	Av. Prueba 123	eyJhcmVhIjogMjQ2OTczLjM2fQ==	eyJjb29yZCI6IFsyMDI3NzYuMTEyNSwgMzUyMDc1Ni43MzI1XSwgWzIwMzAxNS42Mzk0LCAzNTIwNzUyLjA2ODRdLCBbMjAyNzc2LjExMjUsIDM1MjA3NTYuNzMyNV19	https://via.placeholder.com/350x150	2	\N	\N	1
10	00000000-0000-0000-0000-000000000999	GeoServer Test Location	eyJhcmVhIjogMTAwMH0=	W1tbMjIwMDAwLCAzNTIwMjAwXSwgWzIyMDEwLCAzNTIwMjAwXSwgWzIyMDAwLCAzNTIwMzAwXSwgWzIyMDAwLCAzNTIwMjAwXV1d	https://via.placeholder.com/350x150	2	2025-04-24 10:58:42.96117	2025-04-24 10:58:42.96117	1
43	cbeca597-bfd7-473f-85cf-405ad457bea4	REPUBLICA DE ARGENTINA 305, PANAMERICANA, CHIHUAHUA, 31210	eyJhcmVhIjogMjY5LjcxNTI4NTYzODg4NjE0LCAiY29uc3RydWNjaW9uIjogMH0=	W1szOTEwNTMuMTI3MTk5OTk5NzYsMzE2OTk1OC41MjU1OTk5OTk0XSxbMzkxMDg4LjgzMjgsMzE2OTk1Ny4wMzkzOTk5OTk3XSxbMzkxMDg3LjIzNTQwMDAwMDIsMzE2OTk0OS43MTE3XSxbMzkxMDUzLjEyNzE5OTk5OTc2LDMxNjk5NTguNTI1NTk5OTk5NF1d	https://datahub.mpiochih.gob.mx/ows?service=WMS&version=1.3.0&request=GetMap&FORMAT=image/png8&layers=visorurbano:predio_urbano,chih_zonificacion_secundaria_2023,visorurbano:chih_calles_implan,visorurbano:predio_urbano&exceptions=application/vnd.ogc.se_inimage&CRS=EPSG:4326&width=600&height=350&styles=chih_manzanas_catastro,,,chih_predio_detalle&cql_filter=INCLUDE;INCLUDE;INCLUDE;fid=384219&BBOX=28.651643463289645,-106.11531422268196,28.652676650633968,-106.1139240083617	2	2025-04-28 09:52:08.124735	2025-04-28 09:52:08.124735	1
\.


--
-- Data for Name: urban_development_zonings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.urban_development_zonings (id, district, sub_district, publication_date, primary_area_classification_key, primary_area_classification_description, secondary_area_classification_key, secondary_area_classification_description, land_use_key, primary_zone_classification_key, primary_zone_classification_description, secondary_zone_classification_key, secondary_zone_classification_description, area_classification_number, zone_classification_number, zoning_key, restriction, "user", "timestamp", aux, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: urban_development_zonings_standard; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.urban_development_zonings_standard (id, district, sub_district, publication_date, primary_area_classification_key, primary_area_classification_description, secondary_area_classification_key, secondary_area_classification_description, primary_zone_classification_key, primary_zone_classification_description, secondary_zone_classification_key, secondary_zone_classification_description, area_classification_number, zone_classification_number, zoning_key, restriction, municipality_id, geom) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_roles (id, name, description, municipality_id, deleted_at, created_at, updated_at) FROM stdin;
7	citizen	Role for citizens	2	\N	2025-03-19 20:55:13.025242	2025-03-19 20:55:13.025242
8	window_staff	Role for window/counter staff	2	\N	2025-03-19 20:55:13.025242	2025-03-19 20:55:13.025242
9	reviewer	Reviewer role	2	\N	2025-03-19 20:55:13.025242	2025-03-19 20:55:13.025242
10	director	Director role	2	\N	2025-03-19 20:55:13.025242	2025-03-19 20:55:13.025242
11	admin	Administrator role	2	\N	2025-03-19 20:55:13.025242	2025-03-19 20:55:13.025242
12	technician	Technical role	2	\N	2025-03-19 20:55:13.025242	2025-03-19 20:55:13.025242
\.


--
-- Data for Name: user_roles_assignments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_roles_assignments (id, created_at, updated_at, user_id, role_id, pending_role_id, role_status, token) FROM stdin;
1	2025-05-26 16:07:25.635469	2025-05-26 16:40:57.151901	1	7	\N	active	\N
\.


--
-- Data for Name: user_tax_id; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_tax_id (id, tax_id_number, tax_id_type, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, name, email, password, api_token, api_token_expiration, subrole_id, created_at, updated_at, deleted_at, role_id, is_active, paternal_last_name, maternal_last_name, user_tax_id, cellphone, municipality_id, national_id, username, is_staff, is_superuser, last_login, date_joined) FROM stdin;
5	Luis	luis.rodriguez@municipio.gob.mx	$2b$12$LQv3c1yqBwBHV9Z	\N	\N	\N	2025-05-29 11:18:33.667442	2025-05-29 11:18:33.667442	\N	\N	t	Rodríguez	Morales	\N	33-5555-5555	3	\N	\N	f	f	\N	\N
19	Test User 1	test_user_1@example.com	$2b$12$1o4gEgURZlaA1rlmSa/0SeOyvdvU.infLetYAe8lpvMr7Rn44zSPW	\N	\N	\N	2025-05-31 12:54:13.945669	2025-05-31 12:54:13.945669	\N	\N	t	LastName1	\N	\N	1234567890	\N	\N	\N	f	f	\N	\N
20	Test User 2	test_user_2@example.com	$2b$12$dGPa9LQZcQhArC9/4/ueQ.PC/25ifjpPcinLgg/DlSvBDx7O9QkN6	\N	\N	\N	2025-05-31 12:54:13.945669	2025-05-31 12:54:13.945669	\N	\N	t	LastName2	\N	\N	1234567891	\N	\N	\N	f	f	\N	\N
21	Test User 3	test_user_3@example.com	$2b$12$k9YClOYBIQRa8TAm9GtkWeB7Rdcl8QVM4a4aYnL8u9clxnerGo3Z6	\N	\N	\N	2025-05-31 12:54:13.945669	2025-05-31 12:54:13.945669	\N	\N	t	LastName3	\N	\N	1234567892	\N	\N	\N	f	f	\N	\N
22	Test User 4	test_user_4@example.com	$2b$12$r1xWJWkAnN0Dt3oAOzqkUOTzz31l1wZyC7iDiUZzH/s.C5MDYH4Y.	\N	\N	\N	2025-05-31 12:54:13.945669	2025-05-31 12:54:13.945669	\N	\N	t	LastName4	\N	\N	1234567893	\N	\N	\N	f	f	\N	\N
23	Test User 5	test_user_5@example.com	$2b$12$vs.i.ZA0SFnLsXPGv/cJGuhb8oAGGNyphJBHe8v2KA97xcV5Z0vvm	\N	\N	\N	2025-05-31 12:54:13.945669	2025-05-31 12:54:13.945669	\N	\N	t	LastName5	\N	\N	1234567894	\N	\N	\N	f	f	\N	\N
2	Test User	test@example.com	$2b$12$2UyO8j9AZofzIdzhuPOL4.WUYpnQpWO8NZ3wC0RiZEO2DLMPAKvTO	\N	\N	\N	2025-03-10 22:49:22.167627	2025-03-10 22:49:22.167627	\N	7	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
3	Test User	test@example.com	$2b$12$lu/lF1ELNPx/qgK6lPhsl.3XTgRsrVktaSiUFhS66.IWpPcYRZ8SC	\N	\N	\N	2025-03-10 22:49:22.417825	2025-03-10 22:49:22.417825	\N	7	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
4	Updated User	updated@example.com	$2b$12$lPS5zdB931aczx08Pu/PO.B2y0jRVnfekB29QYg8jv3fWwJh3TF0a	\N	\N	\N	2025-03-10 22:49:22.662421	2025-03-10 22:49:22.669459	\N	7	t	Doe	Smith	\N	0987654321	1	\N	\N	f	f	\N	\N
6	Test User	test@example.com	$2b$12$RSWk9nrHN4WPNCgL40Q4eef/uwvWrMy/Ure63grly3.FeWvYPvYKO	\N	\N	\N	2025-03-10 22:49:50.64703	2025-03-10 22:49:50.64703	\N	7	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
7	Test User	test@example.com	$2b$12$.wJ91ULTDwf38nHai.zrjeQiww7qmPIj8JuT9kxkF/G4N/XsP20mK	\N	\N	\N	2025-03-10 22:49:50.895078	2025-03-10 22:49:50.895078	\N	9	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
8	Updated User	updated@example.com	$2b$12$u.acM6YOx.6zJ6/9S86jRepQBrFbtD/O5zNfScNE1NdYq742SFNsK	\N	\N	\N	2025-03-10 22:49:51.138259	2025-03-10 22:49:51.145131	\N	8	t	Doe	Smith	\N	0987654321	1	\N	\N	f	f	\N	\N
13	string	user@example.com	$2b$12$mwZqO3dWn9ZEUWZA0LttguhKbOgAhM9khgIh0h3IxpuKulqlQfMD2	\N	\N	\N	2025-03-12 12:45:06.373444	2025-03-12 12:45:06.373444	\N	7	t	string	string	\N	string	2	\N	\N	f	f	\N	\N
15	Test User	test@example.com	$2b$12$Xk5myFNXqXV3uD7NzzYYseFuBJqv.Ape2POrR7hTeZ/n.m6kFRRWa	\N	\N	\N	2025-03-19 21:12:29.555893	2025-03-19 21:12:29.555893	\N	\N	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
16	Test User	test@example.com	$2b$12$bS2u10q4JDW9mlY1MLr7DeRUpQFBf0NEQcgenxGzOSF.2Y06mQKMO	\N	\N	\N	2025-03-19 21:13:56.171995	2025-03-19 21:13:56.171995	\N	\N	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
17	Test User	test@example.com	$2b$12$o8b.PuagTD7.zDW.ABS7WuXqjqOtyBADcFyd4QqbpOF.qLIkXAeyq	\N	\N	\N	2025-03-19 21:14:49.602994	2025-03-19 21:14:49.602994	\N	\N	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
18	Test User	test@example.com	$2b$12$Lq6KyDFjZj7V83R.InBxeufRPXNt3HM0GHEV8X94LJXKfa/N3MpTS	\N	\N	\N	2025-03-19 21:15:39.719295	2025-03-19 21:15:39.719295	\N	\N	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
1	Luis Medina	niux.legend@gmail.com	$2b$12$wo4c0NFaVCS/WsFR6EuO/urK4xAb9GM5Qr2sba7HywaIdns41zGCy	\N	\N	\N	2025-03-10 22:47:38.393249	2025-03-10 22:47:38.393249	\N	7	t	Doe	Smith	\N	1234567890	1	\N	\N	f	f	\N	\N
\.


--
-- Data for Name: water_body_footprints; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.water_body_footprints (id, area_m2, geom) FROM stdin;
\.


--
-- Data for Name: zoning_control_regulations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.zoning_control_regulations (id, district, regulation_key, land_use, density, intensity, business_sector, minimum_area, minimum_frontage, building_index, land_occupation_coefficient, land_utilization_coefficient, max_building_height, parking_spaces, front_gardening_percentage, front_restriction, lateral_restrictions, rear_restriction, building_mode, observations, municipality_id, urban_environmental_value_areas, planned_public_space, increase_land_utilization_coefficient, hotel_occupation_index) FROM stdin;
1	8	1	Habitacional Unifamiliar	Baja	Media	Residencial	160	8	0.8	0.6	1.2	9	1	30	3	1.5	3	Aislada	Uso habitacional permitido. No se permite comercio.	19	t	f	0.1	1.1
2	8	1	Comercial	Media	Alta	Mixto	200	10	1.0	0.7	1.5	12	2	20	4	2	3	Contigua	Uso comercial con posibilidad de habitacional en niveles superiores.	19	f	t	0.2	1.2
\.


--
-- Data for Name: zoning_impact_level; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.zoning_impact_level (id, impact_level, municipality_id, geom) FROM stdin;
1	2	19	0103000020657F000001000000050000000000000080A808410000000000DB4A410000000020B808410000000000DB4A410000000020B8084100000000FADB4A410000000080A8084100000000FADB4A410000000080A808410000000000DB4A41
\.


--
-- Name: answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.answers_id_seq', 32, true);


--
-- Name: answers_json_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.answers_json_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 1, false);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: base_administrative_division_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.base_administrative_division_id_seq', 1, false);


--
-- Name: base_locality_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.base_locality_id_seq', 1, false);


--
-- Name: base_map_layer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.base_map_layer_id_seq', 1, false);


--
-- Name: base_municipality_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.base_municipality_id_seq', 1, false);


--
-- Name: base_neighborhood_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.base_neighborhood_id_seq', 1, false);


--
-- Name: block_footprints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.block_footprints_id_seq', 1, false);


--
-- Name: blog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_id_seq', 2, true);


--
-- Name: building_footprints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.building_footprints_id_seq', 1, false);


--
-- Name: business_license_histories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_license_histories_id_seq', 6, true);


--
-- Name: business_licenses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_licenses_id_seq', 1, false);


--
-- Name: business_line_configurations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_line_configurations_id_seq', 1, false);


--
-- Name: business_line_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_line_logs_id_seq', 1, false);


--
-- Name: business_lines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_lines_id_seq', 1, false);


--
-- Name: business_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_logs_id_seq', 1, false);


--
-- Name: business_sector_certificates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_sector_certificates_id_seq', 1, false);


--
-- Name: business_sector_configurations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_sector_configurations_id_seq', 1, false);


--
-- Name: business_sector_impacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_sector_impacts_id_seq', 1, false);


--
-- Name: business_sectors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_sectors_id_seq', 1, false);


--
-- Name: business_signatures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_signatures_id_seq', 9, true);


--
-- Name: business_type_configurations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_type_configurations_id_seq', 1627, true);


--
-- Name: business_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.business_types_id_seq', 1093, false);


--
-- Name: dependency_resolutions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.dependency_resolutions_id_seq', 30, true);


--
-- Name: dependency_reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.dependency_reviews_id_seq', 80, true);


--
-- Name: dependency_revisions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.dependency_revisions_id_seq', 65, true);


--
-- Name: economic_activity_base_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.economic_activity_base_id_seq', 1, false);


--
-- Name: economic_activity_sector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.economic_activity_sector_id_seq', 1, false);


--
-- Name: economic_supports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.economic_supports_id_seq', 1, false);


--
-- Name: economic_units_directory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.economic_units_directory_id_seq', 1, false);


--
-- Name: fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.fields_id_seq', 1, false);


--
-- Name: historical_procedures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.historical_procedures_id_seq', 9, true);


--
-- Name: inactive_businesses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.inactive_businesses_id_seq', 1, false);


--
-- Name: issue_resolutions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.issue_resolutions_id_seq', 1, false);


--
-- Name: land_parcel_mapping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.land_parcel_mapping_id_seq', 1, false);


--
-- Name: map_layers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.map_layers_id_seq', 1, false);


--
-- Name: municipalities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.municipalities_id_seq', 1, true);


--
-- Name: municipality_geoms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.municipality_geoms_id_seq', 1, true);


--
-- Name: municipality_map_layer_base_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.municipality_map_layer_base_id_seq', 1, false);


--
-- Name: municipality_signatures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.municipality_signatures_id_seq', 1, false);


--
-- Name: national_id_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.national_id_id_seq', 1, false);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- Name: password_recoveries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.password_recoveries_id_seq', 17, true);


--
-- Name: permit_renewals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.permit_renewals_id_seq', 1, false);


--
-- Name: procedure_registrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.procedure_registrations_id_seq', 16, true);


--
-- Name: procedures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.procedures_id_seq', 130, true);


--
-- Name: provisional_openings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.provisional_openings_id_seq', 16, true);


--
-- Name: public_space_mapping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.public_space_mapping_id_seq', 1, false);


--
-- Name: renewal_file_histories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.renewal_file_histories_id_seq', 1, false);


--
-- Name: renewal_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.renewal_files_id_seq', 1, false);


--
-- Name: renewals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.renewals_id_seq', 1, false);


--
-- Name: requirements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.requirements_id_seq', 1, false);


--
-- Name: requirements_querys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.requirements_querys_id_seq', 5, true);


--
-- Name: reviewers_chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.reviewers_chat_id_seq', 1, false);


--
-- Name: sub_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sub_roles_id_seq', 1, false);


--
-- Name: technical_sheet_downloads_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.technical_sheet_downloads_id_seq', 6, true);


--
-- Name: technical_sheets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.technical_sheets_id_seq', 43, true);


--
-- Name: urban_development_zonings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.urban_development_zonings_id_seq', 1, false);


--
-- Name: urban_development_zonings_standard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.urban_development_zonings_standard_id_seq', 1, false);


--
-- Name: user_roles_assignments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_roles_assignments_id_seq', 1, true);


--
-- Name: user_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_roles_id_seq', 12, true);


--
-- Name: user_tax_id_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_tax_id_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 23, true);


--
-- Name: water_body_footprints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.water_body_footprints_id_seq', 1, false);


--
-- Name: zoning_control_regulations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.zoning_control_regulations_id_seq', 2, true);


--
-- Name: zoning_impact_level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.zoning_impact_level_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: answers_json answers_json_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers_json
    ADD CONSTRAINT answers_json_pkey PRIMARY KEY (id);


--
-- Name: answers answers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: base_administrative_division base_administrative_division_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_administrative_division
    ADD CONSTRAINT base_administrative_division_pkey PRIMARY KEY (id);


--
-- Name: base_locality base_locality_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_locality
    ADD CONSTRAINT base_locality_pkey PRIMARY KEY (id);


--
-- Name: base_map_layer base_map_layer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_map_layer
    ADD CONSTRAINT base_map_layer_pkey PRIMARY KEY (id);


--
-- Name: base_municipality base_municipality_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_municipality
    ADD CONSTRAINT base_municipality_pkey PRIMARY KEY (id);


--
-- Name: base_neighborhood base_neighborhood_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_neighborhood
    ADD CONSTRAINT base_neighborhood_pkey PRIMARY KEY (id);


--
-- Name: block_footprints block_footprints_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.block_footprints
    ADD CONSTRAINT block_footprints_pkey PRIMARY KEY (id);


--
-- Name: blog blog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog
    ADD CONSTRAINT blog_pkey PRIMARY KEY (id);


--
-- Name: building_footprints building_footprints_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_footprints
    ADD CONSTRAINT building_footprints_pkey PRIMARY KEY (id);


--
-- Name: business_license_histories business_license_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_license_histories
    ADD CONSTRAINT business_license_histories_pkey PRIMARY KEY (id);


--
-- Name: business_licenses business_licenses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_licenses
    ADD CONSTRAINT business_licenses_pkey PRIMARY KEY (id);


--
-- Name: business_line_configurations business_line_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_line_configurations
    ADD CONSTRAINT business_line_configurations_pkey PRIMARY KEY (id);


--
-- Name: business_line_logs business_line_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_line_logs
    ADD CONSTRAINT business_line_logs_pkey PRIMARY KEY (id);


--
-- Name: business_lines business_lines_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_lines
    ADD CONSTRAINT business_lines_pkey PRIMARY KEY (id);


--
-- Name: business_logs business_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_logs
    ADD CONSTRAINT business_logs_pkey PRIMARY KEY (id);


--
-- Name: business_sector_certificates business_sector_certificates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_certificates
    ADD CONSTRAINT business_sector_certificates_pkey PRIMARY KEY (id);


--
-- Name: business_sector_configurations business_sector_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_configurations
    ADD CONSTRAINT business_sector_configurations_pkey PRIMARY KEY (id);


--
-- Name: business_sector_impacts business_sector_impacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_impacts
    ADD CONSTRAINT business_sector_impacts_pkey PRIMARY KEY (id);


--
-- Name: business_sectors business_sectors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sectors
    ADD CONSTRAINT business_sectors_pkey PRIMARY KEY (id);


--
-- Name: business_signatures business_signatures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_signatures
    ADD CONSTRAINT business_signatures_pkey PRIMARY KEY (id);


--
-- Name: business_type_configurations business_type_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_type_configurations
    ADD CONSTRAINT business_type_configurations_pkey PRIMARY KEY (id);


--
-- Name: business_types business_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_types
    ADD CONSTRAINT business_types_pkey PRIMARY KEY (id);


--
-- Name: dependency_resolutions dependency_resolutions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_resolutions
    ADD CONSTRAINT dependency_resolutions_pkey PRIMARY KEY (id);


--
-- Name: dependency_reviews dependency_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_reviews
    ADD CONSTRAINT dependency_reviews_pkey PRIMARY KEY (id);


--
-- Name: dependency_revisions dependency_revisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_revisions
    ADD CONSTRAINT dependency_revisions_pkey PRIMARY KEY (id);


--
-- Name: economic_activity_base economic_activity_base_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_activity_base
    ADD CONSTRAINT economic_activity_base_pkey PRIMARY KEY (id);


--
-- Name: economic_activity_sector economic_activity_sector_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_activity_sector
    ADD CONSTRAINT economic_activity_sector_pkey PRIMARY KEY (id);


--
-- Name: economic_supports economic_supports_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_supports
    ADD CONSTRAINT economic_supports_pkey PRIMARY KEY (id);


--
-- Name: economic_units_directory economic_units_directory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_units_directory
    ADD CONSTRAINT economic_units_directory_pkey PRIMARY KEY (id);


--
-- Name: fields fields_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_pkey PRIMARY KEY (id);


--
-- Name: historical_procedures historical_procedures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historical_procedures
    ADD CONSTRAINT historical_procedures_pkey PRIMARY KEY (id);


--
-- Name: inactive_businesses inactive_businesses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inactive_businesses
    ADD CONSTRAINT inactive_businesses_pkey PRIMARY KEY (id);


--
-- Name: issue_resolutions issue_resolutions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_resolutions
    ADD CONSTRAINT issue_resolutions_pkey PRIMARY KEY (id);


--
-- Name: land_parcel_mapping land_parcel_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.land_parcel_mapping
    ADD CONSTRAINT land_parcel_mapping_pkey PRIMARY KEY (id);


--
-- Name: map_layers map_layers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.map_layers
    ADD CONSTRAINT map_layers_pkey PRIMARY KEY (id);


--
-- Name: maplayer_municipality maplayer_municipality_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maplayer_municipality
    ADD CONSTRAINT maplayer_municipality_pkey PRIMARY KEY (maplayer_id, municipality_id);


--
-- Name: municipalities municipalities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipalities
    ADD CONSTRAINT municipalities_pkey PRIMARY KEY (id);


--
-- Name: municipality_geoms municipality_geoms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_geoms
    ADD CONSTRAINT municipality_geoms_pkey PRIMARY KEY (id);


--
-- Name: municipality_map_layer_base municipality_map_layer_base_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_map_layer_base
    ADD CONSTRAINT municipality_map_layer_base_pkey PRIMARY KEY (id);


--
-- Name: municipality_signatures municipality_signatures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_signatures
    ADD CONSTRAINT municipality_signatures_pkey PRIMARY KEY (id);


--
-- Name: national_id national_id_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.national_id
    ADD CONSTRAINT national_id_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: password_recoveries password_recoveries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_recoveries
    ADD CONSTRAINT password_recoveries_pkey PRIMARY KEY (id);


--
-- Name: permit_renewals permit_renewals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permit_renewals
    ADD CONSTRAINT permit_renewals_pkey PRIMARY KEY (id);


--
-- Name: procedure_registrations procedure_registrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedure_registrations
    ADD CONSTRAINT procedure_registrations_pkey PRIMARY KEY (id);


--
-- Name: procedures procedures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedures
    ADD CONSTRAINT procedures_pkey PRIMARY KEY (id);


--
-- Name: provisional_openings provisional_openings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.provisional_openings
    ADD CONSTRAINT provisional_openings_pkey PRIMARY KEY (id);


--
-- Name: public_space_mapping public_space_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.public_space_mapping
    ADD CONSTRAINT public_space_mapping_pkey PRIMARY KEY (id);


--
-- Name: renewal_file_histories renewal_file_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renewal_file_histories
    ADD CONSTRAINT renewal_file_histories_pkey PRIMARY KEY (id);


--
-- Name: renewal_files renewal_files_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renewal_files
    ADD CONSTRAINT renewal_files_pkey PRIMARY KEY (id);


--
-- Name: renewals renewals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renewals
    ADD CONSTRAINT renewals_pkey PRIMARY KEY (id);


--
-- Name: requirements requirements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements
    ADD CONSTRAINT requirements_pkey PRIMARY KEY (id);


--
-- Name: requirements_querys requirements_querys_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements_querys
    ADD CONSTRAINT requirements_querys_pkey PRIMARY KEY (id);


--
-- Name: reviewers_chat reviewers_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviewers_chat
    ADD CONSTRAINT reviewers_chat_pkey PRIMARY KEY (id);


--
-- Name: sub_roles sub_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sub_roles
    ADD CONSTRAINT sub_roles_pkey PRIMARY KEY (id);


--
-- Name: technical_sheet_downloads technical_sheet_downloads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technical_sheet_downloads
    ADD CONSTRAINT technical_sheet_downloads_pkey PRIMARY KEY (id);


--
-- Name: technical_sheets technical_sheets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technical_sheets
    ADD CONSTRAINT technical_sheets_pkey PRIMARY KEY (id);


--
-- Name: urban_development_zonings urban_development_zonings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.urban_development_zonings
    ADD CONSTRAINT urban_development_zonings_pkey PRIMARY KEY (id);


--
-- Name: urban_development_zonings_standard urban_development_zonings_standard_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.urban_development_zonings_standard
    ADD CONSTRAINT urban_development_zonings_standard_pkey PRIMARY KEY (id);


--
-- Name: user_roles_assignments user_roles_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles_assignments
    ADD CONSTRAINT user_roles_assignments_pkey PRIMARY KEY (id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- Name: user_tax_id user_tax_id_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_tax_id
    ADD CONSTRAINT user_tax_id_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: water_body_footprints water_body_footprints_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.water_body_footprints
    ADD CONSTRAINT water_body_footprints_pkey PRIMARY KEY (id);


--
-- Name: zoning_control_regulations zoning_control_regulations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zoning_control_regulations
    ADD CONSTRAINT zoning_control_regulations_pkey PRIMARY KEY (id);


--
-- Name: zoning_impact_level zoning_impact_level_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zoning_impact_level
    ADD CONSTRAINT zoning_impact_level_pkey PRIMARY KEY (id);


--
-- Name: idx_business_line_log_procedure_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_business_line_log_procedure_date ON public.business_line_logs USING btree (procedure_id, created_at);


--
-- Name: idx_business_line_log_type_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_business_line_log_type_date ON public.business_line_logs USING btree (log_type, created_at);


--
-- Name: idx_business_line_log_user_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_business_line_log_user_date ON public.business_line_logs USING btree (user_id, created_at);


--
-- Name: idx_email_token; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_email_token ON public.password_recoveries USING btree (email, token);


--
-- Name: idx_expiration_used; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_expiration_used ON public.password_recoveries USING btree (expiration_date, used);


--
-- Name: ix_business_line_logs_action; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_business_line_logs_action ON public.business_line_logs USING btree (action);


--
-- Name: ix_business_line_logs_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_business_line_logs_created_at ON public.business_line_logs USING btree (created_at);


--
-- Name: ix_business_line_logs_log_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_business_line_logs_log_type ON public.business_line_logs USING btree (log_type);


--
-- Name: ix_business_line_logs_procedure_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_business_line_logs_procedure_id ON public.business_line_logs USING btree (procedure_id);


--
-- Name: ix_business_line_logs_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_business_line_logs_user_id ON public.business_line_logs USING btree (user_id);


--
-- Name: ix_business_line_logs_user_ip; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_business_line_logs_user_ip ON public.business_line_logs USING btree (user_ip);


--
-- Name: ix_password_recoveries_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_password_recoveries_email ON public.password_recoveries USING btree (email);


--
-- Name: ix_password_recoveries_token; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_password_recoveries_token ON public.password_recoveries USING btree (token);


--
-- Name: answers_json answers_json_procedure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers_json
    ADD CONSTRAINT answers_json_procedure_id_fkey FOREIGN KEY (procedure_id) REFERENCES public.procedures(id);


--
-- Name: answers_json answers_json_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers_json
    ADD CONSTRAINT answers_json_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: answers answers_procedure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_procedure_id_fkey FOREIGN KEY (procedure_id) REFERENCES public.procedures(id);


--
-- Name: answers answers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.auth_group(id);


--
-- Name: auth_group_permissions auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id);


--
-- Name: auth_user_groups auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.auth_group(id);


--
-- Name: auth_user_groups auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: authtoken_token authtoken_token_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: base_locality base_locality_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_locality
    ADD CONSTRAINT base_locality_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: base_neighborhood base_neighborhood_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_neighborhood
    ADD CONSTRAINT base_neighborhood_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: block_footprints block_footprints_colony_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.block_footprints
    ADD CONSTRAINT block_footprints_colony_id_fkey FOREIGN KEY (colony_id) REFERENCES public.base_neighborhood(id);


--
-- Name: block_footprints block_footprints_locality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.block_footprints
    ADD CONSTRAINT block_footprints_locality_id_fkey FOREIGN KEY (locality_id) REFERENCES public.base_locality(id);


--
-- Name: block_footprints block_footprints_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.block_footprints
    ADD CONSTRAINT block_footprints_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: building_footprints building_footprints_locality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_footprints
    ADD CONSTRAINT building_footprints_locality_id_fkey FOREIGN KEY (locality_id) REFERENCES public.base_locality(id);


--
-- Name: building_footprints building_footprints_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_footprints
    ADD CONSTRAINT building_footprints_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: building_footprints building_footprints_neighborhood_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.building_footprints
    ADD CONSTRAINT building_footprints_neighborhood_id_fkey FOREIGN KEY (neighborhood_id) REFERENCES public.base_neighborhood(id);


--
-- Name: business_license_histories business_license_histories_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_license_histories
    ADD CONSTRAINT business_license_histories_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: business_license_histories business_license_histories_payment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_license_histories
    ADD CONSTRAINT business_license_histories_payment_user_id_fkey FOREIGN KEY (payment_user_id) REFERENCES public.users(id);


--
-- Name: business_licenses business_licenses_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_licenses
    ADD CONSTRAINT business_licenses_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: business_line_logs business_line_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_line_logs
    ADD CONSTRAINT business_line_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: business_logs business_logs_procedure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_logs
    ADD CONSTRAINT business_logs_procedure_id_fkey FOREIGN KEY (procedure_id) REFERENCES public.procedures(id);


--
-- Name: business_logs business_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_logs
    ADD CONSTRAINT business_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: business_sector_certificates business_sector_certificates_giro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_certificates
    ADD CONSTRAINT business_sector_certificates_giro_id_fkey FOREIGN KEY (business_sector_id) REFERENCES public.business_sectors(id);


--
-- Name: business_sector_certificates business_sector_certificates_municipios_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_certificates
    ADD CONSTRAINT business_sector_certificates_municipios_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: business_sector_configurations business_sector_configurations_business_sector_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_configurations
    ADD CONSTRAINT business_sector_configurations_business_sector_id_fkey FOREIGN KEY (business_sector_id) REFERENCES public.business_sectors(id);


--
-- Name: business_sector_configurations business_sector_configurations_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_configurations
    ADD CONSTRAINT business_sector_configurations_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: business_sector_impacts business_sector_impacts_giro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_impacts
    ADD CONSTRAINT business_sector_impacts_giro_id_fkey FOREIGN KEY (business_sector_id) REFERENCES public.business_sectors(id);


--
-- Name: business_sector_impacts business_sector_impacts_municipio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_sector_impacts
    ADD CONSTRAINT business_sector_impacts_municipio_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: business_signatures business_signatures_procedure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_signatures
    ADD CONSTRAINT business_signatures_procedure_id_fkey FOREIGN KEY (procedure_id) REFERENCES public.procedures(id);


--
-- Name: business_signatures business_signatures_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_signatures
    ADD CONSTRAINT business_signatures_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: business_type_configurations business_type_configurations_business_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_type_configurations
    ADD CONSTRAINT business_type_configurations_business_type_id_fkey FOREIGN KEY (business_type_id) REFERENCES public.business_types(id);


--
-- Name: business_type_configurations business_type_configurations_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_type_configurations
    ADD CONSTRAINT business_type_configurations_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: dependency_resolutions dependency_resolutions_procedure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_resolutions
    ADD CONSTRAINT dependency_resolutions_procedure_id_fkey FOREIGN KEY (procedure_id) REFERENCES public.procedures(id);


--
-- Name: dependency_resolutions dependency_resolutions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_resolutions
    ADD CONSTRAINT dependency_resolutions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: dependency_reviews dependency_reviews_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_reviews
    ADD CONSTRAINT dependency_reviews_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: dependency_reviews dependency_reviews_procedure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_reviews
    ADD CONSTRAINT dependency_reviews_procedure_id_fkey FOREIGN KEY (procedure_id) REFERENCES public.procedures(id);


--
-- Name: dependency_reviews dependency_reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_reviews
    ADD CONSTRAINT dependency_reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: dependency_revisions dependency_revisions_dependency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dependency_revisions
    ADD CONSTRAINT dependency_revisions_dependency_id_fkey FOREIGN KEY (dependency_id) REFERENCES public.requirements_querys(id);


--
-- Name: economic_units_directory economic_units_directory_economic_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_units_directory
    ADD CONSTRAINT economic_units_directory_economic_activity_id_fkey FOREIGN KEY (economic_activity_id) REFERENCES public.economic_activity_base(id);


--
-- Name: economic_units_directory economic_units_directory_locality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_units_directory
    ADD CONSTRAINT economic_units_directory_locality_id_fkey FOREIGN KEY (locality_id) REFERENCES public.base_locality(id);


--
-- Name: economic_units_directory economic_units_directory_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.economic_units_directory
    ADD CONSTRAINT economic_units_directory_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: fields fields_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: inactive_businesses inactive_businesses_giros_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inactive_businesses
    ADD CONSTRAINT inactive_businesses_giros_id_fkey FOREIGN KEY (business_line_id) REFERENCES public.business_lines(id);


--
-- Name: inactive_businesses inactive_businesses_municipios_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inactive_businesses
    ADD CONSTRAINT inactive_businesses_municipios_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: issue_resolutions issue_resolutions_id_tramite_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_resolutions
    ADD CONSTRAINT issue_resolutions_id_tramite_fkey FOREIGN KEY (id_tramite) REFERENCES public.procedures(id);


--
-- Name: issue_resolutions issue_resolutions_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_resolutions
    ADD CONSTRAINT issue_resolutions_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.users(id);


--
-- Name: land_parcel_mapping land_parcel_mapping_locality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.land_parcel_mapping
    ADD CONSTRAINT land_parcel_mapping_locality_id_fkey FOREIGN KEY (locality_id) REFERENCES public.base_locality(id);


--
-- Name: land_parcel_mapping land_parcel_mapping_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.land_parcel_mapping
    ADD CONSTRAINT land_parcel_mapping_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: land_parcel_mapping land_parcel_mapping_neighborhood_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.land_parcel_mapping
    ADD CONSTRAINT land_parcel_mapping_neighborhood_id_fkey FOREIGN KEY (neighborhood_id) REFERENCES public.base_neighborhood(id);


--
-- Name: maplayer_municipality maplayer_municipality_maplayer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maplayer_municipality
    ADD CONSTRAINT maplayer_municipality_maplayer_id_fkey FOREIGN KEY (maplayer_id) REFERENCES public.map_layers(id);


--
-- Name: maplayer_municipality maplayer_municipality_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maplayer_municipality
    ADD CONSTRAINT maplayer_municipality_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: municipality_map_layer_base municipality_map_layer_base_capamapa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_map_layer_base
    ADD CONSTRAINT municipality_map_layer_base_capamapa_id_fkey FOREIGN KEY (map_layer_id) REFERENCES public.base_map_layer(id);


--
-- Name: municipality_map_layer_base municipality_map_layer_base_municipio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_map_layer_base
    ADD CONSTRAINT municipality_map_layer_base_municipio_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: municipality_signatures municipality_signatures_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipality_signatures
    ADD CONSTRAINT municipality_signatures_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: national_id national_id_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.national_id
    ADD CONSTRAINT national_id_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: permit_renewals permit_renewals_id_consulta_requisitos_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permit_renewals
    ADD CONSTRAINT permit_renewals_id_consulta_requisitos_fkey FOREIGN KEY (id_consulta_requisitos) REFERENCES public.requirements_querys(id);


--
-- Name: permit_renewals permit_renewals_id_tramite_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permit_renewals
    ADD CONSTRAINT permit_renewals_id_tramite_fkey FOREIGN KEY (id_tramite) REFERENCES public.procedures(id);


--
-- Name: procedure_registrations procedure_registrations_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedure_registrations
    ADD CONSTRAINT procedure_registrations_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: procedures procedures_requirements_query_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedures
    ADD CONSTRAINT procedures_requirements_query_id_fkey FOREIGN KEY (requirements_query_id) REFERENCES public.requirements_querys(id);


--
-- Name: procedures procedures_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedures
    ADD CONSTRAINT procedures_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: procedures procedures_window_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.procedures
    ADD CONSTRAINT procedures_window_user_id_fkey FOREIGN KEY (window_user_id) REFERENCES public.users(id);


--
-- Name: provisional_openings provisional_openings_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.provisional_openings
    ADD CONSTRAINT provisional_openings_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: provisional_openings provisional_openings_granted_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.provisional_openings
    ADD CONSTRAINT provisional_openings_granted_by_user_id_fkey FOREIGN KEY (granted_by_user_id) REFERENCES public.users(id);


--
-- Name: provisional_openings provisional_openings_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.provisional_openings
    ADD CONSTRAINT provisional_openings_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: provisional_openings provisional_openings_procedure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.provisional_openings
    ADD CONSTRAINT provisional_openings_procedure_id_fkey FOREIGN KEY (procedure_id) REFERENCES public.procedures(id);


--
-- Name: renewal_files renewal_files_renewal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.renewal_files
    ADD CONSTRAINT renewal_files_renewal_id_fkey FOREIGN KEY (renewal_id) REFERENCES public.renewals(id);


--
-- Name: requirements requirements_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements
    ADD CONSTRAINT requirements_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id);


--
-- Name: requirements requirements_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements
    ADD CONSTRAINT requirements_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: requirements_querys requirements_querys_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements_querys
    ADD CONSTRAINT requirements_querys_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: requirements_querys requirements_querys_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.requirements_querys
    ADD CONSTRAINT requirements_querys_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: reviewers_chat reviewers_chat_id_tramite_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviewers_chat
    ADD CONSTRAINT reviewers_chat_id_tramite_fkey FOREIGN KEY (id_tramite) REFERENCES public.procedures(id);


--
-- Name: reviewers_chat reviewers_chat_ir_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviewers_chat
    ADD CONSTRAINT reviewers_chat_ir_usuario_fkey FOREIGN KEY (ir_usuario) REFERENCES public.users(id);


--
-- Name: sub_roles sub_roles_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sub_roles
    ADD CONSTRAINT sub_roles_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: technical_sheet_downloads technical_sheet_downloads_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technical_sheet_downloads
    ADD CONSTRAINT technical_sheet_downloads_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: technical_sheets technical_sheets_id_ficha_tecnica_descarga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technical_sheets
    ADD CONSTRAINT technical_sheets_id_ficha_tecnica_descarga_fkey FOREIGN KEY (technical_sheet_download_id) REFERENCES public.technical_sheet_downloads(id);


--
-- Name: technical_sheets technical_sheets_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.technical_sheets
    ADD CONSTRAINT technical_sheets_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: urban_development_zonings urban_development_zonings_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.urban_development_zonings
    ADD CONSTRAINT urban_development_zonings_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: urban_development_zonings_standard urban_development_zonings_standard_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.urban_development_zonings_standard
    ADD CONSTRAINT urban_development_zonings_standard_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: user_roles_assignments user_roles_assignments_pending_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles_assignments
    ADD CONSTRAINT user_roles_assignments_pending_role_id_fkey FOREIGN KEY (pending_role_id) REFERENCES public.user_roles(id);


--
-- Name: user_roles_assignments user_roles_assignments_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles_assignments
    ADD CONSTRAINT user_roles_assignments_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.user_roles(id);


--
-- Name: user_roles_assignments user_roles_assignments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles_assignments
    ADD CONSTRAINT user_roles_assignments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_roles user_roles_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: user_tax_id user_tax_id_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_tax_id
    ADD CONSTRAINT user_tax_id_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.user_roles(id);


--
-- Name: users users_subrole_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_subrole_id_fkey FOREIGN KEY (subrole_id) REFERENCES public.sub_roles(id);


--
-- Name: zoning_control_regulations zoning_control_regulations_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zoning_control_regulations
    ADD CONSTRAINT zoning_control_regulations_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- Name: zoning_impact_level zoning_impact_level_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.zoning_impact_level
    ADD CONSTRAINT zoning_impact_level_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- PostgreSQL database dump complete
--

