PGDMP  2    #                }            device_registry #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) [    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    37286    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            �           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    37287 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false    5            �            1259    37292    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    5    215            �           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    216            �            1259    37293    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false    5            �            1259    37296    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    5    217            �           0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    218            �            1259    37297    device_presets    TABLE     �   CREATE TABLE public.device_presets (
    id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset_id integer NOT NULL
);
 "   DROP TABLE public.device_presets;
       public         heap    postgres    false    5            �            1259    37300    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false    5            �            1259    37303    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    5    220            �           0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    221            �            1259    37304    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    5    219            �           0    0    device_templates_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_presets.id;
          public          postgres    false    222            �            1259    37305    devices    TABLE     �  CREATE TABLE public.devices (
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
       public         heap    postgres    false    5            �            1259    37311    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    5    223            �           0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    224            �            1259    37312    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false    5            �            1259    37315    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    5    225            �           0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    226            �            1259    37316    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false    5            �            1259    37321    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    5    227            �           0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    228            �            1259    37322    presets    TABLE     �   CREATE TABLE public.presets (
    id integer NOT NULL,
    device_id integer NOT NULL,
    description text,
    role character varying(256) NOT NULL
);
    DROP TABLE public.presets;
       public         heap    postgres    false    5            �            1259    37327    presets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.presets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.presets_id_seq;
       public          postgres    false    5    229            �           0    0    presets_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.presets_id_seq OWNED BY public.presets.id;
          public          postgres    false    230            �            1259    37328 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false    5            �            1259    37333    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    231    5            �           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    232            �            1259    37334 	   templates    TABLE     �   CREATE TABLE public.templates (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    role character varying NOT NULL,
    text text NOT NULL,
    family_id integer
);
    DROP TABLE public.templates;
       public         heap    postgres    false    5            �            1259    37339    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    233    5            �           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    234                        2604    37340    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215                       2604    37341    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217                       2604    37342    device_presets id    DEFAULT     x   ALTER TABLE ONLY public.device_presets ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 @   ALTER TABLE public.device_presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    219                       2604    37343    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220                       2604    37344 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223                       2604    37345    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225                       2604    37346    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227                       2604    37347 
   presets id    DEFAULT     h   ALTER TABLE ONLY public.presets ALTER COLUMN id SET DEFAULT nextval('public.presets_id_seq'::regclass);
 9   ALTER TABLE public.presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229                       2604    37348    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231            	           2604    37349    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    233            �          0    37287 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    215   �h       �          0    37293    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    217   i       �          0    37297    device_presets 
   TABLE DATA           T   COPY public.device_presets (id, template_id, ordered_number, preset_id) FROM stdin;
    public          postgres    false    219   Sm       �          0    37300    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    220   q       �          0    37305    devices 
   TABLE DATA           c   COPY public.devices (id, name, company_id, dev_type, family_id, boot, uboot, firmware) FROM stdin;
    public          postgres    false    223   ]q       �          0    37312    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    225   5r       �          0    37316    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    227   �r       �          0    37322    presets 
   TABLE DATA           C   COPY public.presets (id, device_id, description, role) FROM stdin;
    public          postgres    false    229   �r       �          0    37328 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    231   @s       �          0    37334 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    233   ws       �           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    216            �           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 886, true);
          public          postgres    false    218            �           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 96, true);
          public          postgres    false    221            �           0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 591, true);
          public          postgres    false    222            �           0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 42, true);
          public          postgres    false    224            �           0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 18, true);
          public          postgres    false    226            �           0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    228            �           0    0    presets_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.presets_id_seq', 20, true);
          public          postgres    false    230            �           0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    232            �           0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 385, true);
          public          postgres    false    234                       2606    37351    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    215                       2606    37353    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    217                       2606    37355 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    220                       2606    37357 $   device_presets device_templates_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    219                       2606    37359    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    223                       2606    37361    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    225                       2606    37363    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    225                       2606    37365    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    227                        2606    37367    presets presets_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_pkey;
       public            postgres    false    229            $           2606    37369    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    231            &           2606    37371    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    233                       2606    37373    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    215                       2606    37375    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    223            "           2606    37377    presets unique_device_role 
   CONSTRAINT     `   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT unique_device_role UNIQUE (device_id, role);
 D   ALTER TABLE ONLY public.presets DROP CONSTRAINT unique_device_role;
       public            postgres    false    229    229            (           2606    37379 !   templates unique_family_role_name 
   CONSTRAINT     m   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_family_role_name UNIQUE (family_id, role, name);
 K   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_family_role_name;
       public            postgres    false    233    233    233            )           2606    37380 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    3350    223    217            *           2606    37385 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    217    227    3358            -           2606    37390 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    220    3350    223            .           2606    37395 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    231    3364    220            +           2606    37400 .   device_presets device_templates_preset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_preset_id_fkey FOREIGN KEY (preset_id) REFERENCES public.presets(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_preset_id_fkey;
       public          postgres    false    3360    219    229            ,           2606    37405 0   device_presets device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    3366    219    233            /           2606    37410    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    3340    223    215            0           2606    37415    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    3356    223    225            1           2606    37420    presets presets_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 H   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_device_id_fkey;
       public          postgres    false    229    223    3350            2           2606    37425 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    225    233    3356            �   '   x�3〉�H��21�t�)I��21�t,*MJ����� ���      �   '  x�}�A��6����)|�8bw�ݺK6N0�����#�V,mY�)~�z9m�,_�������~�}�x�������s�L�F�*t�PaNN¥�E�*L�Ra^*���D8I5F.�H.�J.�L.�N.�P.�R.�T.�V!���V�U��	��V�UH+�*��a�ʰ
ieX��2��z�'���
Y�*d��T�Z�����P!+�S�,t.�Ι*䕘%x%�&�hI��ϒH]�%��>K2u}�t��,	��YR��$U�gI��ϒV]���V)��>)��>)��>)��>)��>)��>)���V�UJ+Ǫ��cU�|X��r�JZ9V%���V�UI+Ǫ��cU�*�*iX]�*���U`u�_*�.iX]�*���U`uI�����������������|=�~��|��X|m�հ�_"4¡B��[C����p�
�Ta.a��",�p�j"�B�-��Hl+���
�Ķ�B:�-��Pl+���
IŶ�BZ�-��Vlk��	�)��֔Vlk~Z��y�=�}=�q�cS�(G���
�p���LN�R�"�T�Gک�"*�M"���#�F�(M"Q�4�D��$5J�N�(MBQ�t)E��%5J�V�(]ZQ�t�>a�Ҋ�K+j��i%k�^y�}=���C�����Qo����{އL�[�>�9S�����Cގ�{�a��>,¡�$�I���4�FuJ$jT�T�FuJ&jT�t�FuJ(jTCJQ���ՐVԨ���F5���ՐVԨ���F5���ҊCJi�!�LZqH)�VRʤ��2i�!�LZqH)���ʤ��2i�!�LZqH)�VRʥ��ri�!�\ZqH)�VRʥ��ri�!�\�Ra�ҊCJ���R.�8�TH+)�Vr[����5�?�:�!g�|�F�����?�������ח�wm�{�܌�<����ڌ#���}K�T��(�zǯ/ij��}=s���b�6�����m���˘�8���0�q��/`n�<_���y��t��Ӓ�n�����v��8w+�)���It#�ڌ���6�չ���f���8D�q�*6��܌CTk������q�]��      �   �  x�E�K�� ��0����?�(3��S��L!g�'�z��r�����d]y���M>]0��3_]��'�uŞ)X�EX/�^���\$�"Y�Icu�<�Id}"�,��T�T�.����"�����.���H.�"�x�ŇH.����S$���%�br	��\B.&����%�br	��\B.&��K�'�oq:������z��E9�u�`�[��k;'�z�څ�r�ho�W5IS�U�Uc�����2Uw�]5-O�X5?�X6�j���5ZY;��vS�u��ƺ]뢅�k]4����u)�w�K�k]
�[�x�d�Zף�g��"�{,ˮ~�W�ˎP�e���N�Q{\χ>����=�2���nW��5�����k��{��V�P���WQ���u�^��5NeAa��	�0IX�n�ȇnL��������4�.��������4p8\N����e�4�'����f0��`�M#qӈ�F�5�w�xj�]#�q׈�F�5�w�xj�]#�q׈�^7.����%�r�r	�t��\�\B.].x-���r����t�Kȥ�%���r�r	�t�Ԇ�������Ԇ` �\0�!��+ʞ!��4�`�a�aaO���4#�/��K3B�Ҍ�;�H}�i�4#};�Hs�i�4�w��v��|�)v��r���4#��f�o�i�4#��f���iF��f$�iF��f$��˧cr��N3ҷӌ4w���N3�|�;�d�-I���$阄\��I�%��������� ���� ,�7
A7A7A7A7A7A7A7A7A7�ƍG�HЍH�IЍI��G0NT����y��N`}�L�����MP���N�OЍO�P������ �߶�.�~����f��[��Ԅb ��8J�c8B�����_k�?���      �   A   x����PB���ID?���_G������h*�P����	>��m����Iۘ�����w�r4      �   �   x��P=�0�����R&�&�Fw&(��P��|[��X1Ʀ��޽��p�2j`���d&e��㞸l�B�1F�r8�ő뉍R �z)��*p��I@C4�2���c�)�jb2��C�wA<R2b��;��L��t���:P)��
Z<i5G���9ڢw�2����~��n��\���|-㲹�~�p4����"B< ̑��      �   `   x�ˡ�0EQ�~[��K2�a�`s8L�{x3'y����X�|i�͈�(�2�(��(1a�?��qč�����j��\�z=�x��tND�
�"R      �   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      �   @   x�3�42���LI,I�2�rJ�3��8���2��P^fAn&����	��\�ed ����qqq ! �      �   '   x�3�t���2��())�2����2�,.������� s��      �   �  x��ZYs۶~���VW-}P-y�Ē��8��g<0	Ihť$(E��_,����H[v����M8�98+�e�vd�ֺ�
�Kq0F^�����ި;�h�w�;� ��.��Pk�328�.����[`�gȅȶ����	#����[c/x$��]h�1�f��ir`�9aP|�/�4�B
-/�١�߻��։�2s$����*rtEm��a�%��*��x6�H m�ȏR:��@��F>w���5�k�3W�"o�Z�L�v�j�Yi�uE���1���i5�i�;�(y��y~�:�z>˕���ql��0
"��8`�K�>���rB%AL���$��_��S=W����щ'�w�A����Y(�3b���*��z<>U��<���V�?U��g�Wq��uU����吂������wrۆ�F���9���g���
�R�m�'JQ���f�*��s	3�Q����v�5+yCcï�'������Z�ˏ���sY�/�*g�\=�ʙ�4�H�[`�#�%�d`������x�F�XL�)��n+��%J�,L�.r0t�!��B���l�]+X�������|�o��#�z|��W��~�����`�2���C��,�QX���w����λ+w������I�U�	�9�+��Ͷ�q��M�^(�0/ t)⁃���k3���ص�"=�ǁC�k�K��_�]k��9ȏ��Alg�	�(�}�j��	j��Gq���f�Z�����j��L	jt�cH��Kh�Y�Y�q�E5��}?g�QD	�{>�f�}�mB�7y�VDkt��L��3r���Y'��?&��[ŗژ�&-p�t����^\��ҩ&
B��%s,O�*� �wםn�42ҡ�˛�i����/#:�tz�y@�:���p��C���]BE.��w5V��f���[2U Ku�M��t��u~����%�?�:+6�뒦�UP�������=�	ڶ �݂s���9�e��O��E��t����a�+�3u0^���f��������E�) ¡f&��4��ws+%~�:>�I�'/�"� �h-�|���������k�>���z��nD����0;�]^��1vȘM�w|�b�ec�[��h<��\����k�p�K�lHB.%O�G�x�c�9�1�B��ud�Z��(��l{�?i0ƈF�r �kO ��N�GLR�C#/�[)�ύ+�RyD"�yD~��$33����|Ҍ%����Ċ�罅^/8�.�������gp}|'3us�����%^��H'p����
�kOex��i�u@�Ɖ�T�������j2����nIj�ibn��:�n��v�88\��!`\�]�Kz�طϞ��W��������	
�ϼ����
��Z�k��<�ǖ_
�����Ef�Q��9/N����S14&_�=]\�vn����A�gC�'<]�\w:�^:CLI�t�Ӈި}y��&�/�&5E��)J�aī0b�c$��V�$~� M�ô�Y��Md��քǒ�}P�ڄT��-�m�Nh����;��|'�:��B���A8F�O�λ�ѷ�S�{��k�t��A�}�[R������@�ë��������9���?�v��/7��F����;䆾�!�g|?��3Rq�qF9�+���ռ�R�L���������H`n��l6^E�4��CC݆��� ExF����q��&�U�B4��n��9��jf��2kfafxV��m�n^S�?RomAn_�mQ�B�Ons1=�������OWW�F+�Jw�ZE�:�]0��r0\�+(5�+����+���4Ɲ����fN�x����R��4�P������������k��u�GX�4���~n���k��j4�}��B�������z0���,���j��̌3�֞[ͣV��ڮ]5ܟ����^� ;     