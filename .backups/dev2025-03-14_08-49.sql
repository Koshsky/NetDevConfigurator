PGDMP      1                }           device_registry "   13.14 (Ubuntu 13.14-1.pgdg20.04+1)     16.3 (Ubuntu 16.3-1.pgdg20.04+1) [    /           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            0           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            1           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            2           1262    65697    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            3           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    65698 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false    5            �            1259    65704    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    200    5            4           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    201            �            1259    65706    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false    5            �            1259    65709    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    202    5            5           0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    203            �            1259    65711    device_presets    TABLE     �   CREATE TABLE public.device_presets (
    id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset_id integer NOT NULL
);
 "   DROP TABLE public.device_presets;
       public         heap    postgres    false    5            �            1259    65714    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false    5            �            1259    65717    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    205    5            6           0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    206            �            1259    65719    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    204    5            7           0    0    device_templates_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_presets.id;
          public          postgres    false    207            �            1259    65721    devices    TABLE     �  CREATE TABLE public.devices (
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
       public         heap    postgres    false    5            �            1259    65728    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    5    208            8           0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    209            �            1259    65730    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false    5            �            1259    65733    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    5    210            9           0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    211            �            1259    65735    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false    5            �            1259    65741    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    5    212            :           0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    213            �            1259    65743    presets    TABLE     �   CREATE TABLE public.presets (
    id integer NOT NULL,
    device_id integer NOT NULL,
    description text,
    role character varying(256) NOT NULL
);
    DROP TABLE public.presets;
       public         heap    postgres    false    5            �            1259    65749    presets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.presets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.presets_id_seq;
       public          postgres    false    5    214            ;           0    0    presets_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.presets_id_seq OWNED BY public.presets.id;
          public          postgres    false    215            �            1259    65751 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false    5            �            1259    65757    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    216    5            <           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    217            �            1259    65759 	   templates    TABLE     �   CREATE TABLE public.templates (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    role character varying NOT NULL,
    text text NOT NULL,
    family_id integer
);
    DROP TABLE public.templates;
       public         heap    postgres    false    5            �            1259    65765    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    218    5            =           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    219            d           2604    65767    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    201    200            e           2604    65768    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202            f           2604    65769    device_presets id    DEFAULT     x   ALTER TABLE ONLY public.device_presets ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 @   ALTER TABLE public.device_presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    207    204            g           2604    65770    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    206    205            h           2604    65771 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    209    208            i           2604    65772    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    210            j           2604    65773    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    213    212            k           2604    65774 
   presets id    DEFAULT     h   ALTER TABLE ONLY public.presets ALTER COLUMN id SET DEFAULT nextval('public.presets_id_seq'::regclass);
 9   ALTER TABLE public.presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214            l           2604    65775    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216            m           2604    65776    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218                      0    65698 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    200   �h                 0    65706    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    202   i                 0    65711    device_presets 
   TABLE DATA           T   COPY public.device_presets (id, template_id, ordered_number, preset_id) FROM stdin;
    public          postgres    false    204   �m                 0    65714    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    205   [u       !          0    65721    devices 
   TABLE DATA           c   COPY public.devices (id, name, company_id, dev_type, family_id, boot, uboot, firmware) FROM stdin;
    public          postgres    false    208   �u       #          0    65730    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    210   �v       %          0    65735    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    212   �v       '          0    65743    presets 
   TABLE DATA           C   COPY public.presets (id, device_id, description, role) FROM stdin;
    public          postgres    false    214   ?w       )          0    65751 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    216   �w       +          0    65759 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    218   �w       >           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    201            ?           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 914, true);
          public          postgres    false    203            @           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 96, true);
          public          postgres    false    206            A           0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 836, true);
          public          postgres    false    207            B           0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 42, true);
          public          postgres    false    209            C           0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 18, true);
          public          postgres    false    211            D           0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    213            E           0    0    presets_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.presets_id_seq', 29, true);
          public          postgres    false    215            F           0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    217            G           0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 456, true);
          public          postgres    false    219            p           2606    65778    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    200            t           2606    65780    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    202            x           2606    65782 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    205            v           2606    65784 $   device_presets device_templates_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    204            z           2606    65786    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    208            ~           2606    65788    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    210            �           2606    65790    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    210            �           2606    65792    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    212            �           2606    65794    presets presets_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_pkey;
       public            postgres    false    214            �           2606    65796    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    216            �           2606    65798    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    218            r           2606    65800    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    200            |           2606    65802    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    208            �           2606    65804    presets unique_device_role 
   CONSTRAINT     `   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT unique_device_role UNIQUE (device_id, role);
 D   ALTER TABLE ONLY public.presets DROP CONSTRAINT unique_device_role;
       public            postgres    false    214    214            �           2606    65806 !   templates unique_family_role_name 
   CONSTRAINT     m   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_family_role_name UNIQUE (family_id, role, name);
 K   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_family_role_name;
       public            postgres    false    218    218    218            �           2606    65807 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    2938    202    208            �           2606    65812 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    2946    212    202            �           2606    65817 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    2938    205    208            �           2606    65822 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    2952    205    216            �           2606    65827 .   device_presets device_templates_preset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_preset_id_fkey FOREIGN KEY (preset_id) REFERENCES public.presets(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_preset_id_fkey;
       public          postgres    false    204    214    2948            �           2606    65832 0   device_presets device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    2954    204    218            �           2606    65837    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    2928    208    200            �           2606    65842    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    2944    210    208            �           2606    65847    presets presets_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 H   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_device_id_fkey;
       public          postgres    false    214    2938    208            �           2606    65852 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    2944    210    218               '   x�3〉�H��21�t�)I��21�t,*MJ����� ���         �  x�}�A�]'��q�Uxq���b/�8Q˶du"�������s��\�������x������~��x�������ٯa�B#t:a�0�
�T�$\*\���$�*���&�&�ȥQ�%RGɥR��%S�ɥS�%TGʥT��%U�*��a�ʰ
���
ieX��2�BZV!���V�UH+�*�bQ>���Վ�B;L��u�
Y���1T�B�T!�K�l���-14FSU�L�T�3�R�ϔLU>S:U�L	U�3�T�ϔTU>SZU�LiU��~�jI�*�%��|����YҪ�gI�*�%��|��2���r���r�RZ9V����V�UJ+�*��c��ʱJi�X��r�RZV)��-��-�������*���*���*���*��/+{�|�8�2�|�k��!�k����5�6���¤��v2-����� N¡�E8U��K��0%B#�D�4�X�!�8fH%����ca�t�X�!�8fH)����ca���X�!�8���	�!�8�Vs��d�y�=�}>�q�N�QF��
�p��	�
kΥ�A�*��[��Z�T��]���$B#�D�4���I$�h�T���I&�h�t���I(�h�����K*�h�����K+�h��OX�����K+�h��J���|�k���3{�����UFu�Cf�3�2m���\*d{��{�u���ue��0	�
7�I�F��:�4���I$�(�T���I&�(�t���I(�(�����K*�(�����K+�(��OXuiEe�V�Qvi�%%��⒒]ZqII�V\RҤ��4i�%%MZqII�V\R�t�aeҊKJ��⒒&����I+.)�ҊKJ��⒒.����K+.)�ҊKJ��⒒���ri�%%]ZqII�V\R2������<2�!g��9��x�Y7�lT��߿�?���Ƿ���__j�y���a����x���0�(��}K:��8����q��&�_�3�q��fn�|=�����z������s����6�����m��G��8UR�-�uQ �`V�N+��i�'�%��<�׿߇q���!�~�(�0Q�a���8D9��<��z$1��d���C�^O$����9�H�!�>r���bR��9��s�N5f���0�Ҩ�ӖH�:�I%Z��$��n҉Vg7	E�������MR���&�huv�V�:���d�ҊVgwiE����J��C����=���z]��s���         q  x�E�K��8ץ�L� ��K��Ç�M��2��'9V����_[O,�s������@�W޿ ����������`�W���y��-`'��&�j� $�CX����c�=!L6&��JK���b/��53s�.6 \lB�؂p1\.�K��qi�8.ǥ��4\�����p�tq��P���?^u����O��<�<��Y��|��˹�<��\�����Uy�xYk�h��Kkm~�#��D��Zw���x�Z��d�mc�־�s�R�+�Z���Z�vc�};���Og_�q���(�vOGA�{:
�����#��t��j���p�^�fUg���Z�g���GV����:=C����U�@��v>��W4��W5��W6���]�����k��N�>�p
�r��޹�\�+t�%�&�	����M�����3 �i�"�Ҡu � ҠM �Ҡm K����0�40,���O�߼X	M�M�2�wF�1�Έ#��1���#��1���#��1���#��1��qc�.�K��t\�����qq\:.:N�v\t2���8.ǥ��t\��˹ j��K�l��˹ ��Kh���%tD���K�/��=p�#��G���;!��~i�о4K�/��K���i��o�%��fI�YҺi��o���{�,��4K��fI~�,)n�%��fI�YҼi��n�%�f���4Kj7͒�Y��4K�M�I�8.s�4K�7͒�M��}�L��{F&�{J&�='�h�e�&�.|v��OP�'��T 
*���A�/�_�~a(�š���_$�~�(�Ţ���_4�~�xh��Q�H�/"E���bRT7��QQ)���Uq)����[�)j�"��y�(*:E����S�PѺ���oc��wY�S������i��]��Ԓ�b ��/%A	JHP�j��#�VX=��=��A�O��@�SCp�!;0��YX	�	K0�}�`-A��Ƞ9dP@��i&:=�?iBZЄ6�J{!\ZK2\�A�4�pi��:�K��pir�<�D�.��p1\2�g�f"�pɨΦM
Su�?�T����h���u,ط�Ξ_��X`����-���FX4���U�*�x���VYX�U`QT�E�
,U`Ѭ�VX�����[�*�Ȫ�"���
,�K��FX4���U�*��V�E�
,�/h,x&����@��	`d�t`f�`�I9�����;C7�2�T`���I�:I_�`1�M��qS'i��IZ7u��M�w�6\V���d7u���NR��I�7u��M��y�ߤuc'i���w�7��"�qٸ8.�e��l\����qq\6.�����e�\��%^�h.a.�..�!\b@�Ąp	\.�Kå��[ǥ��qi�t\.=�����D�(�D���J����������E��n��e�	T?0��	̄����N��=�X@K؀%躈jЙ��Ȉ$�rdD*�##���Ȉt~12"�D��!}�ř(�J�)���ݙ����V�%��/�W���Kԫ�D��K4��D��K���ͷ�KԪ�DV�%��/QT�z��h�Lv\&���ə�qY�~�qY��Kd�_"���.K=��Դ� n	�m!����-$X�����=L���Oj�I��6ABw��Xm����&�1eHb��%CC0nb	��QO.�QN��SMJ��
9�lTȿ�*�_F �C4*1D�C�*1D��P���V�!�J�Wb��C�+1D�C4+1D����i��� .��A\��0��{s\��0��{s\��0O��[���ѩ�M�%P��ۜ� �Ձ}[��~o
�m[�g�- ��6�����ϩ��1���M�ϡ�y�F�S��g:f�~�����y��<���         A   x����PB���ID?���_G������h*�P����	>��m����Iۘ�����w�r4      !   �   x��P=�0�����R&�&�Fw&(��P��|[��X1Ʀ��޽��p�2j`���d&e��㞸l�B�1F�r8�ő뉍R �z)��*p��I@C4�2���c�)�jb2��C�wA<R2b��;��L��t���:P)��
Z<i5G���9ڢw�2����~��n��\���|-㲹�~�p4����"B< ̑��      #   `   x�ˡ�0EQ�~[��K2�a�`s8L�{x3'y����X�|i�͈�(�2�(��(1a�?��qč�����j��\�z=�x��tND�
�"R      %   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      '   `   x�M�;
�0D�z�b��	��piDS�q�J��a���8c[�BZ���X �-�U�<q�Z�z���U Pn/Q�tT�\m|���퇮	�+q ���)      )   '   x�3�t���2��())�2����2�,.������� s��      +   c	  x��\[s�F~ƿb��V��t��Z�ˮ�8��g<V2� ����޽� 	�d[I:;����e��9{�h�\{f;��u��xF�9?H_��eoн=k�v.;� �{�p�D����1�``N�9��h����i�@�k�3/2�ch�Q��`��6�G�l�0M	�t� (\��A��X~زCkz���G���h��?��*�1#�mY0״�Q�ڮoC`����j'�T�J��K��&/!�^.\����hw5v��kU���ՖY��r�Q?��A
-��L]� e�e~	�ڇ�R��L���$���0f޿{p�xD�>pE�/�	L�(��o���]��I-U����z4��aJ����z��ƴ�Ѩԑ}<<���q�3 �I>��Wd�F�16���A]�Uyyw٧"w�,�B��3����J9�s</?�8Ћ^(��%^n~�W�3%A�zO)��eV�[�	ǣ �����]���m�x�`�W���.�%w���|��=�v���E�'�X=���DEN��?5=��ƃ B�?�IP���"TS�<�n�9+�H��1'aB0a��.�<4m����Å� zV��FH�o��ӱؿ�3������vz!���`8sg��+,�@�l�M�ݧwp�yw�-��*�M0*��}F�}N�M���t8Y�&r�~H��C~�DK2��w���A�~��g#	�z���\�[���o�r�Y$x�5����&j�m�j�>Y�,|�B�Q�<����Zf�p�qUq�MZ�r
�3� ����*�:�������S��Ȍ���^��|���;���Z��="�Ǐ	���5s��Y�z'�~Lh���/�.M(��(��޷{q�CS�I��[�3�D�4�"p|w��^�ErZtu~58��HB��y��y��Y ��w�VJ�:�A��<e�7-�$A��ʠ�M��Ѕ]`�������7�ywg���iQ��C��C�j�WB�0wm�o�sm�8݂r��IsJ�"��Ӌ8TI@T����W��H\����k���!"�À����#�	CQI�E�����+�{ϝtp�"/�,B��f&�|���ʻ����;���Ի�gx�Q�!�t���@w~�_F�uF��G��ѐ2�/9�!�fdD���̥�.N�r�s�
@�N������#g�ď1�܁R" ��3���,*����'�/�FЌf� �d@�t:�1IE��"��\7Ψj�����%I(fa4!E��D�5W��mǚ�待�V,MW��f��T�0�@��[�Qј�8�l᭩��`[4��8up��=�	O�#����=�iG�.��o��τ�Z4��$���	:"I���%��f�t�9.��6���B/�Rz��o�}�o�!��� ��
�;��3����� Nށ������%���l�'���:`�qrB$p�G����9����n����v����P�	Og׷^v:�^Z�TI�t�Ӈޠ}~��@�W'Jr�T�SԒC��T"o$��II�vM�CY�0K)#ӉzfkJ�A(�&� �m-�[[B�f �l	q���U��#�(��<�H����i�v��z�t�z��n�x{�������V�C�H/ "3<6�dfw(��!�vG��}>��;���q����&m̐��|?y�[-g���zv���jy~ez�Ւ��o���H�����'^U�4j�"�,����T��Ex�^n#��vV�Q^C,ڑ*�@J�R�)�R�Y�Y	����ߦܦ�d�A�o�W5Q�Ay�WnK1}� ����x�?��e� J[�-#B3�M0l�z0ض+(� ʯ+PI,հ^�Űs��J�K&�{]L�J�W���	�m�]�K���d�;�ev�5`.�m{����{ε��������nۗ�ZvP��A�f��6��6P
�،-��m�fӮ3�Mn,=cV���tWl�.���rL�������;a#�0�ُ�W1��r�	[9�t0*n���295�&7n�����Zè��R~��Y�ё�l�������h|��6J�=EY�#�j6z�Ú���(�K���B2��p��,��7�yT��ͦf`��h�G��SX�og#��Q�/00�72���~��T��*�&�Lc�x�7���:��g�<��v&e��>W`�_Y�<yNR��s炀���'�44CT��Qt��'�	u���2CQ5c(KC���24c�P�G�PS{dȚ�����
�84�fkád@UG�e�oٲ(뺩���"l�g'ji�S�45�}�P�=���Hf��F�:B"V�5�+\�e�r'@{ז�'��mԖ��X��#��og4;1I��!.�M���ъ�Yt|&>����*g��������?��     