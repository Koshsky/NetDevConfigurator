PGDMP  )    (                |            device_registry #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) m    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    17557    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false            �            1259    17558 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false            �            1259    17563    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    215            �           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    216            �            1259    17564    device_firmwares    TABLE     �   CREATE TABLE public.device_firmwares (
    id integer NOT NULL,
    device_id integer NOT NULL,
    firmware_id integer NOT NULL
);
 $   DROP TABLE public.device_firmwares;
       public         heap    postgres    false            �            1259    17567    device_firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_firmwares_id_seq;
       public          postgres    false    217            �           0    0    device_firmwares_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_firmwares_id_seq OWNED BY public.device_firmwares.id;
          public          postgres    false    218            �            1259    17568    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false            �            1259    17571    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    219                        0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    220            �            1259    17572    device_presets    TABLE     �   CREATE TABLE public.device_presets (
    id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset_id integer NOT NULL
);
 "   DROP TABLE public.device_presets;
       public         heap    postgres    false            �            1259    17575    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false            �            1259    17578    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    222                       0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    223            �            1259    17579    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    221                       0    0    device_templates_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_presets.id;
          public          postgres    false    224            �            1259    17580    devices    TABLE     Z  CREATE TABLE public.devices (
    id integer NOT NULL,
    name character varying NOT NULL,
    company_id integer NOT NULL,
    dev_type character varying NOT NULL,
    family_id integer NOT NULL,
    CONSTRAINT check_dev_type CHECK (((dev_type)::text = ANY (ARRAY[('router'::character varying)::text, ('switch'::character varying)::text])))
);
    DROP TABLE public.devices;
       public         heap    postgres    false            �            1259    17586    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    225                       0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    226            �            1259    17587    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false            �            1259    17590    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    227                       0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    228            �            1259    17591 	   firmwares    TABLE     �  CREATE TABLE public.firmwares (
    id integer NOT NULL,
    name character varying NOT NULL,
    full_path character varying NOT NULL,
    type character varying NOT NULL,
    CONSTRAINT firmwares_firmware_type_check CHECK (((type)::text = ANY (ARRAY[('primary_bootloader'::character varying)::text, ('secondary_bootloader'::character varying)::text, ('firmware'::character varying)::text])))
);
    DROP TABLE public.firmwares;
       public         heap    postgres    false            �            1259    17597    firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.firmwares_id_seq;
       public          postgres    false    229                       0    0    firmwares_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.firmwares_id_seq OWNED BY public.firmwares.id;
          public          postgres    false    230            �            1259    17598    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false            �            1259    17603    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    231                       0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    232            �            1259    17604    presets    TABLE     d  CREATE TABLE public.presets (
    id integer NOT NULL,
    device_id integer NOT NULL,
    name character varying,
    description text,
    role character varying(256) NOT NULL,
    CONSTRAINT check_role_value CHECK (((role)::text = ANY (ARRAY['data'::text, 'ipmi'::text, 'or'::text, 'tsh'::text, 'video'::text, 'raisa_or'::text, 'raisa_agr'::text])))
);
    DROP TABLE public.presets;
       public         heap    postgres    false            �            1259    17610    presets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.presets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.presets_id_seq;
       public          postgres    false    233                       0    0    presets_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.presets_id_seq OWNED BY public.presets.id;
          public          postgres    false    234            �            1259    17611 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false            �            1259    17616    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    235                       0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    236            �            1259    17617 	   templates    TABLE     �  CREATE TABLE public.templates (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    role character varying NOT NULL,
    text text NOT NULL,
    family_id integer,
    CONSTRAINT check_role_value CHECK (((role)::text = ANY (ARRAY['common'::text, 'data'::text, 'ipmi'::text, 'or'::text, 'tsh'::text, 'video'::text, 'raisa_or'::text, 'raisa_agr'::text]))),
    CONSTRAINT check_type_value CHECK (((type)::text = ANY (ARRAY['header'::text, 'hostname'::text, 'VLAN'::text, 'ssh'::text, 'type-commutation'::text, 'STP'::text, 'credentials'::text, 'addr-set'::text, 'interface'::text, 'GW'::text, 'telnet'::text, 'SNMP'::text, 'ZTP'::text, 'jumbo'::text, 'priority'::text])))
);
    DROP TABLE public.templates;
       public         heap    postgres    false            �            1259    17624    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    237            	           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    238            
           2604    17625    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215                       2604    17626    device_firmwares id    DEFAULT     z   ALTER TABLE ONLY public.device_firmwares ALTER COLUMN id SET DEFAULT nextval('public.device_firmwares_id_seq'::regclass);
 B   ALTER TABLE public.device_firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217                       2604    17627    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219                       2604    17628    device_presets id    DEFAULT     x   ALTER TABLE ONLY public.device_presets ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 @   ALTER TABLE public.device_presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    221                       2604    17629    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    223    222                       2604    17630 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225                       2604    17631    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227                       2604    17632    firmwares id    DEFAULT     l   ALTER TABLE ONLY public.firmwares ALTER COLUMN id SET DEFAULT nextval('public.firmwares_id_seq'::regclass);
 ;   ALTER TABLE public.firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229                       2604    17633    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231                       2604    17634 
   presets id    DEFAULT     h   ALTER TABLE ONLY public.presets ALTER COLUMN id SET DEFAULT nextval('public.presets_id_seq'::regclass);
 9   ALTER TABLE public.presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    233                       2604    17635    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    236    235                       2604    17636    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    238    237            �          0    17558 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    215   ��       �          0    17564    device_firmwares 
   TABLE DATA           F   COPY public.device_firmwares (id, device_id, firmware_id) FROM stdin;
    public          postgres    false    217   0�       �          0    17568    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    219   M�       �          0    17572    device_presets 
   TABLE DATA           T   COPY public.device_presets (id, template_id, ordered_number, preset_id) FROM stdin;
    public          postgres    false    221   |�       �          0    17575    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    222   =�       �          0    17580    devices 
   TABLE DATA           L   COPY public.devices (id, name, company_id, dev_type, family_id) FROM stdin;
    public          postgres    false    225   }�       �          0    17587    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    227   Æ       �          0    17591 	   firmwares 
   TABLE DATA           >   COPY public.firmwares (id, name, full_path, type) FROM stdin;
    public          postgres    false    229   �       �          0    17598    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    231   ��       �          0    17604    presets 
   TABLE DATA           I   COPY public.presets (id, device_id, name, description, role) FROM stdin;
    public          postgres    false    233   G�       �          0    17611 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    235   ��       �          0    17617 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    237   Ј       
           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    216                       0    0    device_firmwares_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_firmwares_id_seq', 32, true);
          public          postgres    false    218                       0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 548, true);
          public          postgres    false    220                       0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 74, true);
          public          postgres    false    223                       0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 480, true);
          public          postgres    false    224                       0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 28, true);
          public          postgres    false    226                       0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 16, true);
          public          postgres    false    228                       0    0    firmwares_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.firmwares_id_seq', 34, true);
          public          postgres    false    230                       0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    232                       0    0    presets_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.presets_id_seq', 12, true);
          public          postgres    false    234                       0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    236                       0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 356, true);
          public          postgres    false    238                       2606    17638    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    215                        2606    17640 &   device_firmwares device_firmwares_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_pkey;
       public            postgres    false    217            $           2606    17642    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    219            (           2606    17644 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    222            &           2606    17646 $   device_presets device_templates_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    221            *           2606    17648    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    225            .           2606    17650    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    227            0           2606    17652    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    227            2           2606    17654 !   firmwares firmwares_full_path_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_full_path_key UNIQUE (full_path);
 K   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_full_path_key;
       public            postgres    false    229            4           2606    17656    firmwares firmwares_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_pkey;
       public            postgres    false    229            8           2606    17658    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    231            :           2606    17660    presets presets_name_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_name_key UNIQUE (name);
 B   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_name_key;
       public            postgres    false    233            <           2606    17662    presets presets_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_pkey;
       public            postgres    false    233            @           2606    17664    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    235            B           2606    17666    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    237                       2606    17668    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    215            "           2606    17670 '   device_firmwares unique_device_firmware 
   CONSTRAINT     t   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT unique_device_firmware UNIQUE (device_id, firmware_id);
 Q   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT unique_device_firmware;
       public            postgres    false    217    217            ,           2606    17672    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    225            6           2606    17674    firmwares unique_firmware_name 
   CONSTRAINT     Y   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT unique_firmware_name UNIQUE (name);
 H   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT unique_firmware_name;
       public            postgres    false    229            >           2606    17676    presets unique_name 
   CONSTRAINT     N   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT unique_name UNIQUE (name);
 =   ALTER TABLE ONLY public.presets DROP CONSTRAINT unique_name;
       public            postgres    false    233            D           2606    17678    templates unique_name_role 
   CONSTRAINT     [   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_name_role UNIQUE (name, role);
 D   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_name_role;
       public            postgres    false    237    237            E           2606    17679 0   device_firmwares device_firmwares_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_device_id_fkey;
       public          postgres    false    3370    225    217            F           2606    17684 2   device_firmwares device_firmwares_firmware_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_firmware_id_fkey FOREIGN KEY (firmware_id) REFERENCES public.firmwares(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_firmware_id_fkey;
       public          postgres    false    3380    229    217            G           2606    17689 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    225    219    3370            H           2606    17694 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    3384    219    231            K           2606    17699 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    225    3370    222            L           2606    17704 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    222    3392    235            I           2606    17709 .   device_presets device_templates_preset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_preset_id_fkey FOREIGN KEY (preset_id) REFERENCES public.presets(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_preset_id_fkey;
       public          postgres    false    3388    221    233            J           2606    17714 0   device_presets device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id);
 Z   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    237    3394    221            M           2606    17719    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    225    215    3356            N           2606    17724    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    3376    227    225            O           2606    17729    presets presets_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 H   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_device_id_fkey;
       public          postgres    false    225    233    3370            P           2606    17734 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    237    3376    227            �   '   x�3〉�H��21�t�)I��21�t,*MJ����� ���      �      x������ � �      �     x�}�;n�@ј{
�@��,ɽ� $%
��q�b\� �9c���x=��_�q>���q~�Ok9��+���RLō�P�)�����F�wE�8�*�*��"��**Y�"�Ut�U�LR�R&*C*��������ee�O�2�rYZ����ʗ�x������^��E�u�]�]f�h�S�e�u6)��AQ��+E}�
D=���>)�5�#�^#�HF�F5�@��Q�R�(��f�T3
��JՌ�jF�V5�D��Q�?�*Ѫf�hU3J�rY%Z���\V�V������a���      �   �  x�E�Ar� C���L��e���S{`�*='q�HM{J���Rm���S�4��=�Kz�VBz�Vw���}ʰ�_�^^k���2���^˲�;�Z������M��������N���$x��	?#��gK�����tv0�A��La3��tv��A��Ja+��tv��A��J��c+4;X����v��`���;�r��iv�Ǘ%���T��}�_}|O%��d���K�J�m)QI�~o*�1�H~\)UR3��Ԍ鑚9]_&_�A��~�#5S1�fl���ۗu���y���3��_9������Ӛ}
ZG gۺY�c��P#!oB3̄nX	ð<���f�|
� ����(<`�
����v@�;�tv� � �A�A��f<�<�`��5W��GMM�#R�Ȩ��GFM3\NH�3� 鑩I�L��47�sAg�c�����Hh�r#�ˍ��ؑ�Eø�H���A,s���3�H�ڙ[��]�'GC+�G��JC���5�p*�p*�8��x���s�kN?����zg�����Yr�9p��.w١���]x�<t��k�Ň��Cw���E�{��>B����$t[	�����Lh�nB�ڧ�����B�t��R���B�4�]�n[��W�6����6~��~��(3_      �   0   x�3��42�4�27 �&\� ڔ�܈��$n���& ڔ+F��� Άs      �   6   x�32��M-6212�41�,.�,I���22�
[�
[���M���b���� �EY      �   K   x�ʱ�0C�Cl�N� �T���ܼ;��u<���ٌ�bfB���Ƣ,�b��26�.5~�}�)�� ~O��      �   �   x�����@Ek�_���j�-�MȪY�̂��
0�Z��='wf�Nl@���)��WK��2�W�� \í�{[��c��]�j@~v����!��|��1�K�
�D��۠�2T
�i�Y7�b��=AU���2��y�׭F�\s�u�~JԺ�k-5B�n�0?���+4S�]�Qmϛk8CO-�O1�L}~!��      �   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      �   B   x�3�42��M-�OI,I����\F0�̂�L�(��2���g���!P�9H����Ր=...  Kd      �   '   x�3�t���2��())�2����2�,.������� s��      �   @  x��X[o9~v~����j�+��@MR%!hRU�*3c�ݹ�づQ���2Bg��FUD��}>���s0Zh'.	/�ː2@��9��x�w������Q��i�Bx@�s&�c`�<�</�aN=@����^	�����K����� �x��ՄLl4%JL~c�h3�q͍��6xZ{FˮИœ�U�� �ڎ��xIk�Ol���"	�4��v�
)v���6��.�5�ɭ�g���c�=�U�*'[���i՜���E�֫I��'/��Q�yA��f5�n��cl��0�I��0��k_baV�	)bˣ�E�X�+�vjT����}q��Z�|�{%�+�|BN{�:�V�y|y*����3V �F�tů���DoC�K�Q����e����Ӎ��
���-;�35rJ�/?�؎
���=�O�U}���+Ho���:��B$.�G�O�/h��ko����=��&8F��� '��0�e�a�0�����V���a[�|�#$(Ơ?��PDzI�j�ϥ���6p(�A^�	$1��1��1r}���,�.āC��j~�����x:�OG�gWщ��۷0�dJ<<�P�'�cI�/;e`��q���Ox�98	f�G�ŏ`��>s�>
~gt�I�^����XF�!%l.󁏜��k�n��c8p9]Sa��\~��xu8'^�Q����e3�17Tć��"|�cQB<ÊB�8�0�B�s7�4��y�!�:<.���t5Kt���;�j�?�fOb��^��9�O��./C�IX�M8��$�j��\L�D}����%�s� O����*q���m����O���:l��7�G�Y��N���h���ϻ}�2,H���;!����)�|��lBb� ��C�!��{�|�;�H�Hm$f3�&���E]�����Q&��rU�%��)�f)~I���i��ŌU̜����Zj#Y2��T��j�[��i��{|/S[ث�n��$�� E��dg[�(E��g(��+K$��9���a�9�?�x�Bn�L2����>^tr��b٣��M�wL��6Y8���V�v�m("��P,��HJ���a9b�d�&h�.�ɂ*��3����</B�"Q)�U�	ۮ�/E2̖�Ty!]�W�%��V��P	�C��(�h������t��L�.K?{�bo��7$��9�æ��wu_��2TS��h�A���a���%1���eu}� �ˀ�x�pI^��2��wx3��`�=HG�����Q�jp_�;�u�g���wֽ�"�:,P��.B�A�ͺ �����D���k�ȋ��1���Q
 �Je62A�b�A��7^<R^n���8$�`
�;+m�/�/տ�"��vD�5�%�N�B#����<��u�Ԉ3C�.N�{t�ى�N�_�����d��>���f����1vY�
ՃS3�K���SS��V�$�Kb��J2���T~J�L���J>q�.�X�a/iH}�#�P�DV�Y���91�,R�݅fUu�Rs!֦��Z�B.:5��P��}��Z�i4���������w�     