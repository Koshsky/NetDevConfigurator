PGDMP                       |            device_registry #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) m    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    34583    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false            �            1259    34584 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false            �            1259    34589    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    217                        0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    218            �            1259    34590    device_firmwares    TABLE     �   CREATE TABLE public.device_firmwares (
    id integer NOT NULL,
    device_id integer NOT NULL,
    firmware_id integer NOT NULL
);
 $   DROP TABLE public.device_firmwares;
       public         heap    postgres    false            �            1259    34593    device_firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_firmwares_id_seq;
       public          postgres    false    219                       0    0    device_firmwares_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_firmwares_id_seq OWNED BY public.device_firmwares.id;
          public          postgres    false    220            �            1259    34594    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false            �            1259    34597    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    221                       0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    222            �            1259    34602    device_presets    TABLE     �   CREATE TABLE public.device_presets (
    id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset_id integer NOT NULL
);
 "   DROP TABLE public.device_presets;
       public         heap    postgres    false            �            1259    34598    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false            �            1259    34601    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    223                       0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    224            �            1259    34605    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    225                       0    0    device_templates_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_presets.id;
          public          postgres    false    226            �            1259    34606    devices    TABLE     Z  CREATE TABLE public.devices (
    id integer NOT NULL,
    name character varying NOT NULL,
    company_id integer NOT NULL,
    dev_type character varying NOT NULL,
    family_id integer NOT NULL,
    CONSTRAINT check_dev_type CHECK (((dev_type)::text = ANY (ARRAY[('router'::character varying)::text, ('switch'::character varying)::text])))
);
    DROP TABLE public.devices;
       public         heap    postgres    false            �            1259    34612    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    227                       0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    228            �            1259    34613    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false            �            1259    34616    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    229                       0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    230            �            1259    34617 	   firmwares    TABLE     �  CREATE TABLE public.firmwares (
    id integer NOT NULL,
    name character varying NOT NULL,
    full_path character varying NOT NULL,
    type character varying NOT NULL,
    CONSTRAINT firmwares_firmware_type_check CHECK (((type)::text = ANY (ARRAY[('primary_bootloader'::character varying)::text, ('secondary_bootloader'::character varying)::text, ('firmware'::character varying)::text])))
);
    DROP TABLE public.firmwares;
       public         heap    postgres    false            �            1259    34623    firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.firmwares_id_seq;
       public          postgres    false    231                       0    0    firmwares_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.firmwares_id_seq OWNED BY public.firmwares.id;
          public          postgres    false    232            �            1259    34624    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false            �            1259    34629    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    233                       0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    234            �            1259    34750    presets    TABLE     d  CREATE TABLE public.presets (
    id integer NOT NULL,
    device_id integer NOT NULL,
    name character varying,
    description text,
    role character varying(256) NOT NULL,
    CONSTRAINT check_role_value CHECK (((role)::text = ANY (ARRAY['data'::text, 'ipmi'::text, 'or'::text, 'tsh'::text, 'video'::text, 'raisa_or'::text, 'raisa_agr'::text])))
);
    DROP TABLE public.presets;
       public         heap    postgres    false            �            1259    34749    presets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.presets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.presets_id_seq;
       public          postgres    false    240            	           0    0    presets_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.presets_id_seq OWNED BY public.presets.id;
          public          postgres    false    239            �            1259    34630 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false            �            1259    34635    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    235            
           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    236            �            1259    34636 	   templates    TABLE     �  CREATE TABLE public.templates (
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
       public         heap    postgres    false            �            1259    34643    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    237                       0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    238                       2604    34644    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217                       2604    34645    device_firmwares id    DEFAULT     z   ALTER TABLE ONLY public.device_firmwares ALTER COLUMN id SET DEFAULT nextval('public.device_firmwares_id_seq'::regclass);
 B   ALTER TABLE public.device_firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219                       2604    34646    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    221                       2604    34648    device_presets id    DEFAULT     x   ALTER TABLE ONLY public.device_presets ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 @   ALTER TABLE public.device_presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225                       2604    34647    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223                       2604    34649 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227                       2604    34650    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229                       2604    34651    firmwares id    DEFAULT     l   ALTER TABLE ONLY public.firmwares ALTER COLUMN id SET DEFAULT nextval('public.firmwares_id_seq'::regclass);
 ;   ALTER TABLE public.firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231                       2604    34652    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    233                       2604    34753 
   presets id    DEFAULT     h   ALTER TABLE ONLY public.presets ALTER COLUMN id SET DEFAULT nextval('public.presets_id_seq'::regclass);
 9   ALTER TABLE public.presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    239    240    240                       2604    34653    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    236    235                       2604    34654    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    238    237            �          0    34584 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    217   �       �          0    34590    device_firmwares 
   TABLE DATA           F   COPY public.device_firmwares (id, device_id, firmware_id) FROM stdin;
    public          postgres    false    219   %�       �          0    34594    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    221   B�       �          0    34602    device_presets 
   TABLE DATA           T   COPY public.device_presets (id, template_id, ordered_number, preset_id) FROM stdin;
    public          postgres    false    225   ��       �          0    34598    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    223   H�       �          0    34606    devices 
   TABLE DATA           L   COPY public.devices (id, name, company_id, dev_type, family_id) FROM stdin;
    public          postgres    false    227   r�       �          0    34613    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    229   ��       �          0    34617 	   firmwares 
   TABLE DATA           >   COPY public.firmwares (id, name, full_path, type) FROM stdin;
    public          postgres    false    231   �       �          0    34624    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    233   �       �          0    34750    presets 
   TABLE DATA           I   COPY public.presets (id, device_id, name, description, role) FROM stdin;
    public          postgres    false    240   <�       �          0    34630 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    235   ��       �          0    34636 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    237   Ɉ                  0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    218                       0    0    device_firmwares_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_firmwares_id_seq', 32, true);
          public          postgres    false    220                       0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 436, true);
          public          postgres    false    222                       0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 62, true);
          public          postgres    false    224                       0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 319, true);
          public          postgres    false    226                       0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 28, true);
          public          postgres    false    228                       0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 16, true);
          public          postgres    false    230                       0    0    firmwares_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.firmwares_id_seq', 34, true);
          public          postgres    false    232                       0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    234                       0    0    presets_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.presets_id_seq', 6, true);
          public          postgres    false    239                       0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    236                       0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 356, true);
          public          postgres    false    238                       2606    34656    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    217            "           2606    34658 &   device_firmwares device_firmwares_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_pkey;
       public            postgres    false    219            &           2606    34660    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    221            (           2606    34662 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    223            *           2606    34664 $   device_presets device_templates_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    225            ,           2606    34666    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    227            0           2606    34668    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    229            2           2606    34670    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    229            4           2606    34672 !   firmwares firmwares_full_path_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_full_path_key UNIQUE (full_path);
 K   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_full_path_key;
       public            postgres    false    231            6           2606    34674    firmwares firmwares_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_pkey;
       public            postgres    false    231            :           2606    34676    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    233            B           2606    34759    presets presets_name_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_name_key UNIQUE (name);
 B   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_name_key;
       public            postgres    false    240            D           2606    34757    presets presets_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_pkey;
       public            postgres    false    240            <           2606    34678    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    235            >           2606    34680    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    237                        2606    34682    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    217            $           2606    34684 '   device_firmwares unique_device_firmware 
   CONSTRAINT     t   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT unique_device_firmware UNIQUE (device_id, firmware_id);
 Q   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT unique_device_firmware;
       public            postgres    false    219    219            .           2606    34686    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    227            8           2606    34688    firmwares unique_firmware_name 
   CONSTRAINT     Y   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT unique_firmware_name UNIQUE (name);
 H   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT unique_firmware_name;
       public            postgres    false    231            F           2606    34772    presets unique_name 
   CONSTRAINT     N   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT unique_name UNIQUE (name);
 =   ALTER TABLE ONLY public.presets DROP CONSTRAINT unique_name;
       public            postgres    false    240            @           2606    34775    templates unique_name_role 
   CONSTRAINT     [   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_name_role UNIQUE (name, role);
 D   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_name_role;
       public            postgres    false    237    237            G           2606    34691 0   device_firmwares device_firmwares_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_device_id_fkey;
       public          postgres    false    3372    227    219            H           2606    34696 2   device_firmwares device_firmwares_firmware_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_firmware_id_fkey FOREIGN KEY (firmware_id) REFERENCES public.firmwares(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_firmware_id_fkey;
       public          postgres    false    219    3382    231            I           2606    34701 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    227    3372    221            J           2606    34706 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    3386    221    233            K           2606    34711 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    223    227    3372            L           2606    34716 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    223    3388    235            M           2606    34765 .   device_presets device_templates_preset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_preset_id_fkey FOREIGN KEY (preset_id) REFERENCES public.presets(id);
 X   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_preset_id_fkey;
       public          postgres    false    225    240    3396            N           2606    34726 0   device_presets device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id);
 Z   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    3390    237    225            O           2606    34731    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    227    3358    217            P           2606    34736    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    227    3378    229            R           2606    34760    presets presets_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 H   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_device_id_fkey;
       public          postgres    false    227    3372    240            Q           2606    34741 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    237    3378    229            �   '   x�3〉�H��21�t�)I��21�t,*MJ����� ���      �      x������ � �      �   �   x�}�1�0D��>' ���I�$+�I�|1�fR�b����$�i۷�k}�����V%���T#TtFW1C��XUl�MŉqRqf�U\�����F�FF$H$����	����d���2JAJ� ��V�V��K+����h��
������#{\�s�^�s�]t��=���z�      �   :  x�=�ˑ#1Cϭ`�DR�\&�8 ���L5h�t�/|}�Y�a�ߋ�� O�N�x�E=������z}a��7>��L}���[����oS��Ǔ�������أ �}�5l��%���t�S���f���7#� QXN5��QxN5��QxN5��QxN5��QxN0j�	b�2}�F�������2��|4j��W>z0s�"=���&m��h�^w�������x�A��$��M�7�ơ�⿔7%:�vzi�+M���x�4-�(M�3K��0�Ų�wiڞS����*��K��Zi�^/M���{Gi��Y���|���|���|���|���_֖`
���l��#�}�F�,X	���	����;k�� �����]��
���� k�P�ՍY{+ity?죽_�Ϩ�F�BDa�S�A/�U�Qa���v��W���##�"�ȑ�r�s�~!P���}1@��r����$��EA=�a*�R��8Gy��D�H�L�PC������Ȅ�M&�2�j��k�	���ڵ̈́�:����u�Q&,�3aע� �� �j��ķ��>\�L�O��0U?�w����l�ͮh�M�@����=�5V����P��2�ފ�(�@�<�Mq@�Ҁ�=��R�[I@}���\9Xs���M����͛��w��n�:�MP�w����z7A�u��� \��v��t�MB7A�	��M�n��u���	Wŏ��y��z��{B�|�ڧ��O��O�- ���
 ���~[@��ahS�@X���*�v�p����k���"v      �      x�33�42�4�23Ѧ\1z\\\ "�      �   6   x�32��M-6212�41�,.�,I���22�
[�
[���M���b���� �EY      �   K   x�ʱ�0C�Cl�N� �T���ܼ;��u<���ٌ�bfB���Ƣ,�b��26�.5~�}�)�� ~O��      �   �   x�����@Ek�_���j�-�MȪY�̂��
0�Z��='wf�Nl@���)��WK��2�W�� \í�{[��c��]�j@~v����!��|��1�K�
�D��۠�2T
�i�Y7�b��=AU���2��y�׭F�\s�u�~JԺ�k-5B�n�0?���+4S�]�Qmϛk8CO-�O1�L}~!��      �   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      �   F   x�3�42��M-�OI,I����\F0�̂�L�(��2���g���	X���Ռ��(`����� �wf      �   '   x�3�t���2��())�2����2�,.������� s��      �   5  x��X[s�8~V~������of�4�$���&�Nf:���o�eX��_]|!��B��tRlK���I��c�i�V��ʾ
(�g����A@�x~9�\�o�t��� �w>�ь0{r38�>�ȅ�u�v��E>D����3a�34cg�b�!q�C�P첊�)���C��oA�#� �8����@�@oZ%�Y4�]%�A1ԲmEK�>��l/p0DhiD=T�)v���;�}�k��["�@�	�c�=ߩ�eN�1g�V+���/��VN��y���r���]P6�)o�6z>ƦL���  �����CL�w�VB,���H��^�O�S�T�S����S/�_x�ƛ��l�����56Wj�>	�<�Z܈��3V �V�4ůh��Do�#�w��5�\���e�Bp��VU�
�wrˎ�L��Ҝ��'.�>�S��G�ImU�ih�
�;*�vι��
����;�Z[E��:�{OlǷN�34���</�y�i3kU�fZ�j��2S�&����?P�Ap�����UK,�h�Z���Sb�QjG����ЛF��CE��:�6�����><?���w�t����Ϯ�3㟷oaHɔ�x���w Ò@_(���Q��G���}t���N���o|��>���:�H�n�M'A$�p��6���Cv���p7��1�;��VSb��\�e���η]N��0	�M����B�Ȯ,§��%�S�0p�=_ 3��lb�&��
��������T�Q��;��(�RE�+M|`�ښY��\k�*�\����,�j�Q�H�Z`���pq1C�p�b^�^x�(WF�LRv�*l�Y�')V�a�`
&�'1|�.&��y��GdS�[�V�����~�N1���߰�.y�1�&�î��П"��n����	)�V�Ua;�e�w^0Ő�c��>�������|��a����˔�L��Ie$FS���G� �\�.U㦜�"7]%`��)���3������3�v��BM��,�J��U�������_˨-���?.��bRS�2X$���s�he�t6�Tb�T�3���iF�@e�h�Q�e�LR�Z>��}�lg,MŲG?��w�.��+�ڈݪ�+"��R,�JPZZ[��q1b�d�h9�ɂ�d����ܞ�[b�����ʀ�eU�/�R̦�Ty!]�zW���f-G�8�u-�h*&9���75��L�*K�V�7���S��q�U�x߻~�jZ�!Qy4e����u���lJL�ajQS.��"`+^$\�k䮼��b+�;<���p0I/�#�w����s=x��w{�����]t�H0� �om��(@�~�)@�  ��Q�Z��5�bo3� #XK��^*fK ��g �
���ڑ�rK���M�	��H�Ғ�2A��{��K+B��h�D'oP�8�-�\o/�~ﯣF��3�����GǼ�=lw�����Ѿ��GF|�/�"Y-�n-a;����P]85���#é�P^�Bp�-���%��eb?%x&G4Hx;�Ӓږ:`��ER?y/<�C5���U���u&     