PGDMP      "                }            device_registry "   13.14 (Ubuntu 13.14-1.pgdg20.04+1)     16.3 (Ubuntu 16.3-1.pgdg20.04+1) [    0           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            1           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            2           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            3           1262    40960    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            4           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    40961 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false    5            �            1259    40967    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    200    5            5           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    201            �            1259    40969    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false    5            �            1259    40972    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    202    5            6           0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    203            �            1259    40974    device_presets    TABLE     �   CREATE TABLE public.device_presets (
    id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset_id integer NOT NULL
);
 "   DROP TABLE public.device_presets;
       public         heap    postgres    false    5            �            1259    40977    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false    5            �            1259    40980    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    205    5            7           0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    206            �            1259    40982    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    204    5            8           0    0    device_templates_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_presets.id;
          public          postgres    false    207            �            1259    40984    devices    TABLE     �  CREATE TABLE public.devices (
    id integer NOT NULL,
    name character varying NOT NULL,
    company_id integer NOT NULL,
    dev_type character varying NOT NULL,
    family_id integer NOT NULL,
    boot character varying,
    uboot character varying,
    firmware character varying,
    CONSTRAINT check_dev_type CHECK (((dev_type)::text = ANY (ARRAY[('router'::character varying)::text, ('switch'::character varying)::text])))
);
    DROP TABLE public.devices;
       public         heap    postgres    false    5            �            1259    40991    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    5    208            9           0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    209            �            1259    40993    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false    5            �            1259    40996    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    5    210            :           0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    211            �            1259    40998    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false    5            �            1259    41004    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    212    5            ;           0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    213            �            1259    41006    presets    TABLE     �   CREATE TABLE public.presets (
    id integer NOT NULL,
    device_id integer NOT NULL,
    description text,
    role character varying(256) NOT NULL
);
    DROP TABLE public.presets;
       public         heap    postgres    false    5            �            1259    41012    presets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.presets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.presets_id_seq;
       public          postgres    false    214    5            <           0    0    presets_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.presets_id_seq OWNED BY public.presets.id;
          public          postgres    false    215            �            1259    41014 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false    5            �            1259    41020    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    216    5            =           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    217            �            1259    41022 	   templates    TABLE       CREATE TABLE public.templates (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    role character varying NOT NULL,
    text text NOT NULL,
    family_id integer,
    CONSTRAINT check_type_value CHECK (((type)::text = ANY (ARRAY['hostname'::text, 'VLAN'::text, 'ssh'::text, 'type-commutation'::text, 'STP'::text, 'credentials'::text, 'addr-set'::text, 'interface'::text, 'GW'::text, 'telnet'::text, 'SNMP'::text, 'ZTP'::text, 'jumbo'::text, 'priority'::text])))
);
    DROP TABLE public.templates;
       public         heap    postgres    false    5            �            1259    41029    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    5    218            >           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    219            d           2604    41031    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    201    200            e           2604    41032    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202            f           2604    41033    device_presets id    DEFAULT     x   ALTER TABLE ONLY public.device_presets ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 @   ALTER TABLE public.device_presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    207    204            g           2604    41034    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    206    205            h           2604    41035 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    209    208            i           2604    41036    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    210            j           2604    41037    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    213    212            k           2604    41038 
   presets id    DEFAULT     h   ALTER TABLE ONLY public.presets ALTER COLUMN id SET DEFAULT nextval('public.presets_id_seq'::regclass);
 9   ALTER TABLE public.presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214            l           2604    41039    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216            m           2604    41040    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218                      0    40961 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    200   �i                 0    40969    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    202   j                 0    40974    device_presets 
   TABLE DATA           T   COPY public.device_presets (id, template_id, ordered_number, preset_id) FROM stdin;
    public          postgres    false    204   �m                 0    40977    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    205   �q       "          0    40984    devices 
   TABLE DATA           c   COPY public.devices (id, name, company_id, dev_type, family_id, boot, uboot, firmware) FROM stdin;
    public          postgres    false    208   Dr       $          0    40993    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    210   �r       &          0    40998    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    212   Ss       (          0    41006    presets 
   TABLE DATA           C   COPY public.presets (id, device_id, description, role) FROM stdin;
    public          postgres    false    214   �s       *          0    41014 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    216   �s       ,          0    41022 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    218   (t       ?           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    201            @           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 844, true);
          public          postgres    false    203            A           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 96, true);
          public          postgres    false    206            B           0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 584, true);
          public          postgres    false    207            C           0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 37, true);
          public          postgres    false    209            D           0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 17, true);
          public          postgres    false    211            E           0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    213            F           0    0    presets_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.presets_id_seq', 20, true);
          public          postgres    false    215            G           0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    217            H           0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 363, true);
          public          postgres    false    219            q           2606    41042    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    200            u           2606    41044    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    202            y           2606    41046 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    205            w           2606    41048 $   device_presets device_templates_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    204            {           2606    41050    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    208                       2606    41052    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    210            �           2606    41054    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    210            �           2606    41056    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    212            �           2606    41058    presets presets_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_pkey;
       public            postgres    false    214            �           2606    41060    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    216            �           2606    41062    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    218            s           2606    41064    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    200            }           2606    41066    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    208            �           2606    41068    presets unique_device_role 
   CONSTRAINT     `   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT unique_device_role UNIQUE (device_id, role);
 D   ALTER TABLE ONLY public.presets DROP CONSTRAINT unique_device_role;
       public            postgres    false    214    214            �           2606    41070    templates unique_name_role 
   CONSTRAINT     [   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_name_role UNIQUE (name, role);
 D   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_name_role;
       public            postgres    false    218    218            �           2606    41071 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    2939    208    202            �           2606    41076 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    202    212    2947            �           2606    41081 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    205    2939    208            �           2606    41086 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    205    216    2953            �           2606    41091 .   device_presets device_templates_preset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_preset_id_fkey FOREIGN KEY (preset_id) REFERENCES public.presets(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_preset_id_fkey;
       public          postgres    false    214    204    2949            �           2606    41096 0   device_presets device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    204    2955    218            �           2606    41101    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    2929    200    208            �           2606    41106    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    210    208    2945            �           2606    41111    presets presets_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 H   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_device_id_fkey;
       public          postgres    false    214    208    2939            �           2606    41116 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    2945    210    218               '   x�3〉�H��21�t�)I��21�t,*MJ����� ���         k  x�}�1�9DQ��:�n��$�w�#���?�9v�������r���땯_����������||~��m����NaZ����A8-����EX�p_#nE�I��P�R(RC)T����p
uj@�B5�B�T�T�T��U�U�*�=a�jձJ��X�Zu�R�:V�V�T��U��b�ϸ-䶣Y�eG������������a!�B�9��<�Q���N��T�S��H�>S�N}�2��Lu:��
u�3U��g*թ�T�S��V�>��VK�N}�Z��,�:�Yju����g�թ�R���R��j�U`UjX���R����*�*�
�J��R����*�*�J�J���V��V��j�/V[���V��V��j�Ub���������_�]���~������5�����X�|mH�	��˷����$� L'�pN�pY�	KnR'�(Ո�0S�3U��0S�3Չ�0S�3U��0S�3Պ�0S�s�{�j�ca�b,��e�5�#�s�x����!�k5:6�F����pX���s�p���p[���o��Y�	�"ܤN�QW#j��"Q��U���L�huu�F�+5Z�R�h�RQ�jE�V�5Z��	�P+j�B��ъ/+�ъz����!���r�?S8�Fg�9����!Ǟ�><g.yg��yg���Ug���Y�	�"ܤN�HՈխHԨnU�Fu+5�[��Q�
E���5��TԨ�ZQ�jjE���{ª�5��VԨ�Z��TS+��jjŒR]�XR��KJu�bI��V,)�Պ%�����V,)�Պ%��Z��TW+��
�bI�P+��
�bI�P+��
�bI�P+��
���*Ԋ%�B�XR*Ԋ%�R�XR*��t,T���;g<��:�!���?�u��B�         L  x�E�Ir�0���L�X����Ǡ�D���l7R���������q���z=����[��'Y���x:��/o�`]�홬��=�u�n/�a�0�ݗ���+`��l?L���h420��CF�!�����`��h0e`4�20L���C�)�������`���V$E��h�ʠ^�i��7��e=�����ܾ�U�7�*�i��˲(�|����\��X%�&1ê��/^��M5ڄ�F���)��F�;�T��E��1T�oL֦��s��[�G�����s���qV������kg]/A#��]��!�$a	�K^����� 
`�4���� `�4��h�%� K��@����d`40LN<��@���ǨqE�ƨ��ƨ�TcԩQF��aԸ8�z��&���aҩ�;&�[�sA�ms��-�A�-n!�h�[5��BͶ�8a�p�`�{aB_\;��[��5з�ｸ�8l'��p5�J_���N�p*~L Gp\ Gpl
⤹���3�$p28��\N�7۠��݄�n�A7堛s�M:�ft��y��+�wAwAw	AwAwA�W��2��YG�<	Zg%��{���Z��,&��j��,'�'�.(�(�.)�i�|Ϟ���P�T�[�=1���ړ�HR����7�e��;a_N���&���:��I.��
�4V�䁣���'�L�L�T�T]򕋽"�X��L$s�\,Dr��źH.6Dr�)��ɥ������rirq�4��\�\\.M..�&�K��˥������r1��\L.!�K���r1��\L.!�K���r1��\L.!�K���rq��\\.)\������}���rq��\\.)�K�wm�c���:�.ܳպ�m}|�o��t��e��-�_��a~�#�/v�|���;�}�#�;B�ؑrǎ�w�Hcǎ4w�Hk���;R۱#َ�w�H�cG�;R߱#�;�ܱ#�;�xw�Hmǎd;v$߱#iM\.Ck�r}ǎ4v�Hsǎ�v�@Sk�r�Z��Ԛ�\����2�&A�����?k�
B         A   x����PB���ID?���_G������h*�P����	>��m����Iۘ�����w�r4      "   �   x���A� E��]���Tp���c�0^� ���qBf�_��j�ـ�XAx��|�}Ѥ�i��'�"��� �u��#_�� ����.9�r�d�r����d�f-�8�?�6�3B�HvlN_�l�(s�w�h=(�<A�'V[XgL[x��+r�      $   Q   x��1� D�Z!�X��6��qi��·����"�����"(����h�N��tc&Qܸ٨�m��2�{����~[@?      &   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      (   C   x�3�42���LI,I�2�r2r3������.C��9\��1�Vgh�il�%�r�� rb���� 61�      *   '   x�3�t���2��())�2����2�,.������� s��      ,     x��Y[s�8~V~���-����M�IB6д��LG��ŗ�2,�俯.� ���f:�m�|��t��'l4-Њ]�:�e���r0h~/oݻ��v��e�	B��C�	s&!7�c�c��M���p6E>D�Mm�0����f1
萸.���G(����)�g�C���A�#� ���>�o@��h�%�h�\�P�qp�y����C$��Z�C坹�C��Y9�������*S��5���c/��VY�m��Դr�<�q�*I��I�W��(�|���e���N���1�dq���w	�T�������������&G�͎��:�K�{N��:���W�|{x'�N>���B��>�^_�����>��
�؉�������������n��r�t٧#&8�t'S���'���y����99�����@n+z+���i�v�=I��s��;D��zDy��Ƈ���N�p��������6�9bx���p�|.� b��v"�`v�k'�0l+�o�~�|������)�(/IS�����@��Ŝ#h�q���<�Y�\��0DQ4����Eȸ�?����ѿ�;������]xa���)��)c��Ȱ$�W��"�AT����ϧx�9���m��g0�[_�s_r��|I���7��Hf�%l!끇�$�kS���ǰ�r��2 ��#<5���d����w��x�Ca�,�+����B���S[�OQ#�3J��Xa0%�b	L�P��Y����"Đ���Ъ�������]���?o�e�b����Ws�$1��N��L]'f56��Ǔ�|��a�����ej+�U>��Dkj� �|�"!>��U�F�Լդ&T��02�����*�ǝ֠u��Xy�����8����D��D�jC9��e���<��-���?��`RW�B�+8y|�Y���3؀'��Y�+��j�f�@%�O4ު�>(��F˛���7����X������Ӵ�A�fbi���د�uEDl�E.B���s��#�l���RY,��5^��d���N/:	9�l�&4l�D|�~�b6%������
�(@��UT�R� rԍ��<��ɝd*���H�0d����T��*boHLQ2�U�_��ػ{:��"TS��l�@W��&��y�$����H<��0��΀�	��<�ב+��.�����Brz��ݻ�S����^���U�)�� @�ֶ�7�4 ����
PD�m�s�a��F
+F�3;��߿ � ?p�;���SY�'	'�B�#�N՘m��������.������ oP�8�-��������_��8s����۰G�\�K�;�~�9�����G�##������U�����#��RP
8�33�Kξ+�3S���D�sK,�����B\&�3��E������j�i����(C�+?��0b1�P5�j��]��L�'&^��$����E��@���Wȹ�WOV���,�Z�7ҙR[�e���n��[n��Ze幀�2����r���Qu��u�����r�^�J���o{�X7+_<���{#�prtt�?zY.     