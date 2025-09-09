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

