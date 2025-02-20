PGDMP                      }            device_registry #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) Z    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    20112    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            �           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    20113 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false    5            �            1259    20118    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    5    215            �           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    216            �            1259    20119    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false    5            �            1259    20122    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    217    5            �           0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    218            �            1259    20123    device_presets    TABLE     �   CREATE TABLE public.device_presets (
    id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset_id integer NOT NULL
);
 "   DROP TABLE public.device_presets;
       public         heap    postgres    false    5            �            1259    20126    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false    5            �            1259    20129    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    220    5            �           0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    221            �            1259    20130    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    219    5            �           0    0    device_templates_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_presets.id;
          public          postgres    false    222            �            1259    20131    devices    TABLE     �  CREATE TABLE public.devices (
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
       public         heap    postgres    false    5            �            1259    20137    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    223    5            �           0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    224            �            1259    20138    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false    5            �            1259    20141    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    5    225            �           0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    226            �            1259    20142    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false    5            �            1259    20147    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    5    227            �           0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    228            �            1259    20148    presets    TABLE     �   CREATE TABLE public.presets (
    id integer NOT NULL,
    device_id integer NOT NULL,
    description text,
    role character varying(256) NOT NULL
);
    DROP TABLE public.presets;
       public         heap    postgres    false    5            �            1259    20153    presets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.presets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.presets_id_seq;
       public          postgres    false    229    5            �           0    0    presets_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.presets_id_seq OWNED BY public.presets.id;
          public          postgres    false    230            �            1259    20154 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false    5            �            1259    20159    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    231    5            �           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    232            �            1259    20160 	   templates    TABLE       CREATE TABLE public.templates (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    role character varying NOT NULL,
    text text NOT NULL,
    family_id integer,
    CONSTRAINT check_type_value CHECK (((type)::text = ANY (ARRAY['hostname'::text, 'VLAN'::text, 'ssh'::text, 'type-commutation'::text, 'STP'::text, 'credentials'::text, 'addr-set'::text, 'interface'::text, 'GW'::text, 'telnet'::text, 'SNMP'::text, 'ZTP'::text, 'jumbo'::text, 'priority'::text])))
);
    DROP TABLE public.templates;
       public         heap    postgres    false    5            �            1259    20166    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    233    5            �           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    234                        2604    20167    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215                       2604    20168    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217                       2604    20169    device_presets id    DEFAULT     x   ALTER TABLE ONLY public.device_presets ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 @   ALTER TABLE public.device_presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    219                       2604    20170    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220                       2604    20171 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223                       2604    20172    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225                       2604    20173    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227                       2604    20174 
   presets id    DEFAULT     h   ALTER TABLE ONLY public.presets ALTER COLUMN id SET DEFAULT nextval('public.presets_id_seq'::regclass);
 9   ALTER TABLE public.presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229                       2604    20175    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231            	           2604    20176    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    233            �          0    20113 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    215   �h       �          0    20119    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    217   �h       �          0    20123    device_presets 
   TABLE DATA           T   COPY public.device_presets (id, template_id, ordered_number, preset_id) FROM stdin;
    public          postgres    false    219   m       �          0    20126    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    220   �q       �          0    20131    devices 
   TABLE DATA           c   COPY public.devices (id, name, company_id, dev_type, family_id, boot, uboot, firmware) FROM stdin;
    public          postgres    false    223   �q       �          0    20138    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    225   �r       �          0    20142    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    227   (s       �          0    20148    presets 
   TABLE DATA           C   COPY public.presets (id, device_id, description, role) FROM stdin;
    public          postgres    false    229   ss       �          0    20154 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    231   �s       �          0    20160 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    233   �s       �           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    216            �           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 886, true);
          public          postgres    false    218            �           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 96, true);
          public          postgres    false    221            �           0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 591, true);
          public          postgres    false    222            �           0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 42, true);
          public          postgres    false    224            �           0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 18, true);
          public          postgres    false    226            �           0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    228            �           0    0    presets_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.presets_id_seq', 20, true);
          public          postgres    false    230            �           0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    232            �           0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 369, true);
          public          postgres    false    234                       2606    20178    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    215                       2606    20180    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    217                       2606    20182 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    220                       2606    20184 $   device_presets device_templates_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    219                       2606    20186    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    223                       2606    20188    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    225                       2606    20190    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    225                       2606    20192    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    227            !           2606    20194    presets presets_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_pkey;
       public            postgres    false    229            %           2606    20196    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    231            '           2606    20198    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    233                       2606    20200    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    215                       2606    20202    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    223            #           2606    20204    presets unique_device_role 
   CONSTRAINT     `   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT unique_device_role UNIQUE (device_id, role);
 D   ALTER TABLE ONLY public.presets DROP CONSTRAINT unique_device_role;
       public            postgres    false    229    229            (           2606    20205 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    223    217    3351            )           2606    20210 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    3359    217    227            ,           2606    20215 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    223    220    3351            -           2606    20220 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    220    231    3365            *           2606    20225 .   device_presets device_templates_preset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_preset_id_fkey FOREIGN KEY (preset_id) REFERENCES public.presets(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_preset_id_fkey;
       public          postgres    false    219    229    3361            +           2606    20230 0   device_presets device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    219    3367    233            .           2606    20235    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    3341    215    223            /           2606    20240    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    223    225    3357            0           2606    20245    presets presets_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 H   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_device_id_fkey;
       public          postgres    false    3351    229    223            1           2606    20250 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    3357    225    233            �   '   x�3〉�H��21�t�)I��21�t,*MJ����� ���      �   '  x�}�A��6����)|�8bw�ݺK6N0�����#�V,mY�)~�z9m�,_�������~�}�x�������s�L�F�*t�PaNN¥�E�*L�Ra^*���D8I5F.�H.�J.�L.�N.�P.�R.�T.�V!���V�U��	��V�UH+�*��a�ʰ
ieX��2��z�'���
Y�*d��T�Z�����P!+�S�,t.�Ι*䕘%x%�&�hI��ϒH]�%��>K2u}�t��,	��YR��$U�gI��ϒV]���V)��>)��>)��>)��>)��>)��>)���V�UJ+Ǫ��cU�|X��r�JZ9V%���V�UI+Ǫ��cU�*�*iX]�*���U`u�_*�.iX]�*���U`uI�����������������|=�~��|��X|m�հ�_"4¡B��[C����p�
�Ta.a��",�p�j"�B�-��Hl+���
�Ķ�B:�-��Pl+���
IŶ�BZ�-��Vlk��	�)��֔Vlk~Z��y�=�}=�q�cS�(G���
�p���LN�R�"�T�Gک�"*�M"���#�F�(M"Q�4�D��$5J�N�(MBQ�t)E��%5J�V�(]ZQ�t�>a�Ҋ�K+j��i%k�^y�}=���C�����Qo����{އL�[�>�9S�����Cގ�{�a��>,¡�$�I���4�FuJ$jT�T�FuJ&jT�t�FuJ(jTCJQ���ՐVԨ���F5���ՐVԨ���F5���ҊCJi�!�LZqH)�VRʤ��2i�!�LZqH)���ʤ��2i�!�LZqH)�VRʥ��ri�!�\ZqH)�VRʥ��ri�!�\�Ra�ҊCJ���R.�8�TH+)�Vr[����5�?�:�!g�|�F�����?�������ח�wm�{�܌�<����ڌ#���}K�T��(�zǯ/ij��}=s���b�6�����m���˘�8���0�q��/`n�<_���y��t��Ӓ�n�����v��8w+�)���It#�ڌ���6�չ���f���8D�q�*6��܌CTk������q�]��      �   p  x�E�I��0��c&D,\���Ǡ�L��@�m1MPPu��x�?}�X���c���Q�O��O
���}�`�;뙂U��g	6a�K诨��M$��"Y�Ic�H{�$��H&[&]*[*�.���^�\���b&���H."�X��bC$�"��������r�rq�t��\�\\.]..�.�K��˥������@���7�}o~���j^�e]���Vױ�΅�~W��F��W��ū�DW�U�Tc����"T'�T�E˓5V����R�uc�F+kgUc�쪱n�j��Z-l�u��6��R@�ZJ�k)��%~y�k-��ѳVw���X�]��W��W�e���N�Q{\�}j����X�����V����U���u-V6�u]�z0YC7'�d�Y��;�t�p�\{�.>���Op���?�~���@�����`��h0e`4�20,��KF�%�A���|CF̜:>u���o�Q��v�^��F���u�K�>X����n�u�ڬ��Yo��7~A
:a�0NX� lWG�ʲsyt���5 �5 е��������������h`20��&�^�?4�+7����D0�k���h�uMQ�MQ�MQ�MQ�MQ�MQ�MQ�MQ�Mt�K���rq��\\.)�K���r���5��[7r���rq��\\.)�K�%^Η!��0C.�!�1C.�;`<C.��@��D����� ���pn¹C �����~����@�Hyi��@�'0��	�}h�'0��	$;���'0��R��@'0��	�ui�� ��	�~�N` �	$���1q��qi��@Z'0��	�������Σ��c�rY:&A���-������0 7c n� ܜ�I�e�������/q����R���/y�������E�K �/����r�K"����мy�n"�I��{S	��\��L@~�	(n:}��%ЗQ@��>�~�«��m|k���T=�! � ����/A����P|}g�S\��!���{�pA�G���	��m])"�K�~)�$������B��(��]��[��Y�����������q      �   A   x����PB���ID?���_G������h*�P����	>��m����Iۘ�����w�r4      �   �   x��P=�0�����R&�&�Fw&(��P��|[��X1Ʀ��޽��p�2j`���d&e��㞸l�B�1F�r8�ő뉍R �z)��*p��I@C4�2���c�)�jb2��C�wA<R2b��;��L��t���:P)��
Z<i5G���9ڢw�2����~��n��\���|-㲹�~�p4����"B< ̑��      �   `   x�ˡ�0EQ�~[��K2�a�`s8L�{x3'y����X�|i�͈�(�2�(��(1a�?��qč�����j��\�z=�x��tND�
�"R      �   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      �   C   x�3�42���LI,I�2�r2r3������.C��9\��1�Vgh�il�%�r�� rb���� 61�      �   '   x�3�t���2��())�2����2�,.������� s��      �   H  x��Y[s�8~V~���-���CXH�t��4�t2�� w�K3�頋/@m�SH3���t>}G:�����Ď�ڷ���)&cdc��>^����w�g_/{O��h�R{238�>&h�l,��3�C�8PWv�	c���;「\��>t��3��6%���eP��{AJ�B;�Nd���>��f��4���.[��(��6����P�m/p0Dh�E>���;:$�5���[�C�k���L������ܪeA�3g]Q�9�8���$���vC�}���r·H�}P��)�ڍ^��!�Ð���{H����}��~P�'�r�S��1�;��d�����}u���7�����N�*�|FM{�>�+}�__�����>��
@��O�����Y�j.�����j�>]���1��b*��$�8/t��>'�����>=��ۉ���D�:g�YAzOn�-p�ܨ�ր��ɡ�Y+��|��Ƿ���矀x^�3�IS���U91؅f�}B���?��`x����45(kK,4t:`�(Q͢� �0񑇡7���>Q-�@��dR���ew�n���C�r�~q^���{C����`��Ȱ�W��"�ad}B���S<�^��凮y�3�䭂/̹/��?h���Y��A$�0���t)ꁇ�$�3��9��b�aTEf@�������ƛߞ1��I�x��l�6a�Gvc>E�0�(n�b��̵�+`��|�u��$��A�!�n�cy	+�U/����	��y�-{Lu���~{�A2�xȋԵcڠSF|2M���C썂��E'��/S[���Ic�[S��gsq�	�:7�� �!4��}��s,|��9p��;�y���\�_�Ӂ�r �K�HRTI�V1���_�����ҕ�������j& U	����ǜE!Z?M�Y�
,�ſ2�WC�32�~��V��A��6J�4���e,ɲO$?V �����2+#UM�~��$��K��f�8k#�l���Q,� V�6d���N�;q9�l�:�L��~�b����恫
U+@5��W�R� 1ԭ��<��əf*�P�H�0d�l��T��(b�	L^2�u�_��ؿ{:Q�"T]��l�@���6��y6����H<��s0��̀W	��<�7�+��ADy��iz!9��Ǐݳ��S���;�b�w����4�f���]Z"nvh �S�#����X�b��6�P0��� �Rgj�`0� � ?p�;���Q�'�N1�G���1� ���[�/�]�B����Aܠ�2�)ZQ�?]]���N[�k/�盋o�>�0�/�>������}�=w�:?�>�r0y�6|��XJ.gp�'v��w�p�K#�Q ��+?��x�/����E�.�˱�Ր�b�g>/C�+?��1�1�P6�j���]��L�'&^1�$����y��@����ȹ��Oօ��,�Zηҙ�[�e���n`�;nVA�2��C��V��9%�\���u����._��_�[�D������^�B��_���iL�`�o����-&�)��?8Uax�=���G<�����<z89::�3���     