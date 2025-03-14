PGDMP      1                }            device_registry "   13.14 (Ubuntu 13.14-1.pgdg20.04+1)     16.3 (Ubuntu 16.3-1.pgdg20.04+1) [    /           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
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
    public          postgres    false    204   Om                 0    65714    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    205   q       !          0    65721    devices 
   TABLE DATA           c   COPY public.devices (id, name, company_id, dev_type, family_id, boot, uboot, firmware) FROM stdin;
    public          postgres    false    208   Yq       #          0    65730    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    210   1r       %          0    65735    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    212   �r       '          0    65743    presets 
   TABLE DATA           C   COPY public.presets (id, device_id, description, role) FROM stdin;
    public          postgres    false    214   �r       )          0    65751 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    216   <s       +          0    65759 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    218   ss       >           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    201            ?           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 886, true);
          public          postgres    false    203            @           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 96, true);
          public          postgres    false    206            A           0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 591, true);
          public          postgres    false    207            B           0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 42, true);
          public          postgres    false    209            C           0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 18, true);
          public          postgres    false    211            D           0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    213            E           0    0    presets_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.presets_id_seq', 21, true);
          public          postgres    false    215            F           0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    217            G           0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 443, true);
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
       public          postgres    false    2944    210    218               '   x�3〉�H��21�t�)I��21�t,*MJ����� ���         '  x�}�A��6����)|�8bw�ݺK6N0�����#�V,mY�)~�z9m�,_�������~�}�x�������s�L�F�*t�PaNN¥�E�*L�Ra^*���D8I5F.�H.�J.�L.�N.�P.�R.�T.�V!���V�U��	��V�UH+�*��a�ʰ
ieX��2��z�'���
Y�*d��T�Z�����P!+�S�,t.�Ι*䕘%x%�&�hI��ϒH]�%��>K2u}�t��,	��YR��$U�gI��ϒV]���V)��>)��>)��>)��>)��>)��>)���V�UJ+Ǫ��cU�|X��r�JZ9V%���V�UI+Ǫ��cU�*�*iX]�*���U`u�_*�.iX]�*���U`uI�����������������|=�~��|��X|m�հ�_"4¡B��[C����p�
�Ta.a��",�p�j"�B�-��Hl+���
�Ķ�B:�-��Pl+���
IŶ�BZ�-��Vlk��	�)��֔Vlk~Z��y�=�}=�q�cS�(G���
�p���LN�R�"�T�Gک�"*�M"���#�F�(M"Q�4�D��$5J�N�(MBQ�t)E��%5J�V�(]ZQ�t�>a�Ҋ�K+j��i%k�^y�}=���C�����Qo����{އL�[�>�9S�����Cގ�{�a��>,¡�$�I���4�FuJ$jT�T�FuJ&jT�t�FuJ(jTCJQ���ՐVԨ���F5���ՐVԨ���F5���ҊCJi�!�LZqH)�VRʤ��2i�!�LZqH)���ʤ��2i�!�LZqH)�VRʥ��ri�!�\ZqH)�VRʥ��ri�!�\�Ra�ҊCJ���R.�8�TH+)�Vr[����5�?�:�!g�|�F�����?�������ח�wm�{�܌�<����ڌ#���}K�T��(�zǯ/ij��}=s���b�6�����m���˘�8���0�q��/`n�<_���y��t��Ӓ�n�����v��8w+�)���It#�ڌ���6�չ���f���8D�q�*6��܌CTk������q�]��         �  x�E�K�� ��0����?�(3��S��L!g�'�z��r�����d]y���M>]0��3_]��'�uŞ)X�EX/�^���\$�"Y�Icu�<�Id}"�,��T�T�.����"�����.���H.�"�x�ŇH.����S$���%�br	��\B.&����%�br	��\B.&��K�'�oq:������z��E9�u�`�[��k;'�z�څ�r�ho�W5IS�U�Uc�����2Uw�]5-O�X5?�X6�j���5ZY;��vS�u��ƺ]뢅�k]4����u)�w�K�k]
�[�x�d�Zף�g��"�{,ˮ~�W�ˎP�e���N�Q{\χ>����=�2���nW��5�����k��{��V�P���WQ���u�^��5NeAa��	�0IX�n�ȇnL��������4�.��������4p8\N����e�4�'����f0��`�M#qӈ�F�5�w�xj�]#�q׈�F�5�w�xj�]#�q׈�^7.����%�r�r	�t��\�\B.].x-���r����t�Kȥ�%���r�r	�t�Ԇ�������Ԇ` �\0�!��+ʞ!��4�`�a�aaO���4#�/��K3B�Ҍ�;�H}�i�4#};�Hs�i�4�w��v��|�)v��r���4#��f�o�i�4#��f���iF��f$�iF��f$��˧cr��N3ҷӌ4w���N3�|�;�d�-I���$阄\��I�%��������� ���� ,�7
A7A7A7A7A7A7A7A7A7�ƍG�HЍH�IЍI��G0NT����y��N`}�L�����MP���N�OЍO�P������ �߶�.�~����f��[��Ԅb ��8J�c8B�����_k�?���         A   x����PB���ID?���_G������h*�P����	>��m����Iۘ�����w�r4      !   �   x��P=�0�����R&�&�Fw&(��P��|[��X1Ʀ��޽��p�2j`���d&e��㞸l�B�1F�r8�ő뉍R �z)��*p��I@C4�2���c�)�jb2��C�wA<R2b��;��L��t���:P)��
Z<i5G���9ڢw�2����~��n��\���|-㲹�~�p4����"B< ̑��      #   `   x�ˡ�0EQ�~[��K2�a�`s8L�{x3'y����X�|i�͈�(�2�(��(1a�?��qč�����j��\�z=�x��tND�
�"R      %   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      '   @   x�3�42���LI,I�2�rJ�3��8���2��P^fAn&����	��\�ed ����qqq ! �      )   '   x�3�t���2��())�2����2�,.������� s��      +   �  x��[Ys�H~��Y�nptr��>���@�T�U.Y@YtD���9$�@���V
G��|}L�t�%�О�s��:^ L;@�X�p��>]�F��E���p�y����K3Ч.n'�F�6��l�,�3͆�a@Y(]��@�L���b�x��a h��gA��ɀu&�"�_�����5���{�7�:�Zj�ā?���\-�ں�|Kjp�m9��*a�trI�w�l����%�kf3��"��Z�L���zU�2��<˂��3�c�%�b6Ӧk�Gɳ���K8�!X��Y�F�ǱB��7��9��#z��A*�NVL�D���A�(ł��O�L���щ���A������v�2�re��ODQ w$οb q�'2���_�=�.�7��R�(/�.�D����br(?��6�W��1��y���Dv�B	\)��!o�)�j�J��s4�O�<\�=h��wU.oh1��q���&����V��#��rl�vAϙ
g�\?��$U�ڷ���l۴'#!0�F(dx	�j.[Hh��@�f)0��5��ȳ5Ak�k�e���|�xD��� �����|"o��#�z|��W���	]�\�34AP�XcQ��i`#��Q��~z�;o����ݹ��c|��3�s,��������Z6	�;>�2�!�Vt<�4=4����f���60��<�E�ebװW������m}��Y�:��ឍ�&��\�I�m�G�>�E�GX�33����>�+��$���\M���*�HV9EVl��EQU0���q��-0qߓz5}�Ch���S���A-�b�'���ͭG����	��Ǩ-�V��6&�Q���:����v/LsX�T�	!s|=0�
�U�N�;��i\��E7�7�Ӑ�,n��3��z*�, i�X�>��qQ�=j��C`����Ƹ8�hʦ0ؼS9��3�2̕��aƻ?����z�5�MI��J[��F��Es*�5A�0<���W�n�=i����E*��"U2�T���p�
�T�W�ǦG<���o�<�O�E7�)�|I��U���-���m����60�T�7>������m
���>���<��	74��Nw��.�L��Y�W��)|82b�%A�G���hd������DÅ��f@�w��D��vs�"�a�����D�&��I��Z� @3wO�_����=YA4�)$���t?�&91DP�b��BH�0�*GrGؗd$a��ф�Ǔf(y]�޶0���ܷ��9K������޺��0S���[���1g:gio��`��#����D�5�'b���$��: ^�Dn�q���7��^5GH��lI b7�h���e�ó�^<�L�+[�;0��B;pY{��ώ�h���a	F!���-Tp>s����� Nߡ���ȜGw0�m�6#=��lԁ�`N�� ��=�����o؉�.�?u;���h� �����.����;�n/�A�DK:��CoԾ�܄��73�r���S��C	��0�1U�HI"��4[� k35K�j6a��Ix()�1k�+����4 ��T� ��	i��P����"(�F�1�7x�t���kO���C�}�����(�U)8�c9��)@t�Ǉ�Ș����?�6�����L�7�zb�'���g�yg������Ʒ^Έť���.+^(Լ�V=��������$P�Wi���E�z�"�"n�%���)ix�^b#&�����l!��He 5TM�eVM�L�W��MnSɟ)�� ����(U�$+�������d|ӂ��-E����=Ǘ��.�l9��5���e(�$eJX/McĹ�t%53&�]L�K�W��	Q���hf������O���7k<�\�����k��Ϝk`U�)�R=���RzP����A-���l��Ԕ5�V���Q��ڴ+E�*7��	�?���+����u	"�M��٠�%�dl���#�h%(��o$RH��ʹ��O�$�hU�q�MD�����-ه���P*�.AFJ�Q���.TX�F�Ø%�Q��)�4a8	�iV<��-O��%�x��]Hn9�_��� Q�f7����ɔ,Jx���Hur*ρ�b2R�:���F�|����	Ae�$�58/��G�U�Aw6����~""#rx�K�aL������_����     