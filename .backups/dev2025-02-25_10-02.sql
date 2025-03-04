PGDMP          
            }            device_registry "   13.14 (Ubuntu 13.14-1.pgdg20.04+1)     16.3 (Ubuntu 16.3-1.pgdg20.04+1) [    /           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            0           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            1           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            2           1262    49152    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            3           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    5            �            1259    49153 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false    5            �            1259    49159    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    200    5            4           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    201            �            1259    49161    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false    5            �            1259    49164    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    202    5            5           0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    203            �            1259    49166    device_presets    TABLE     �   CREATE TABLE public.device_presets (
    id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset_id integer NOT NULL
);
 "   DROP TABLE public.device_presets;
       public         heap    postgres    false    5            �            1259    49169    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false    5            �            1259    49172    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    205    5            6           0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    206            �            1259    49174    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    5    204            7           0    0    device_templates_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_presets.id;
          public          postgres    false    207            �            1259    49176    devices    TABLE     �  CREATE TABLE public.devices (
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
       public         heap    postgres    false    5            �            1259    49183    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    208    5            8           0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    209            �            1259    49185    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false    5            �            1259    49188    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    5    210            9           0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    211            �            1259    49190    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false    5            �            1259    49196    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    212    5            :           0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    213            �            1259    49198    presets    TABLE     �   CREATE TABLE public.presets (
    id integer NOT NULL,
    device_id integer NOT NULL,
    description text,
    role character varying(256) NOT NULL
);
    DROP TABLE public.presets;
       public         heap    postgres    false    5            �            1259    49204    presets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.presets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.presets_id_seq;
       public          postgres    false    5    214            ;           0    0    presets_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.presets_id_seq OWNED BY public.presets.id;
          public          postgres    false    215            �            1259    49206 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false    5            �            1259    49212    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    5    216            <           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    217            �            1259    49214 	   templates    TABLE     �   CREATE TABLE public.templates (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    role character varying NOT NULL,
    text text NOT NULL,
    family_id integer
);
    DROP TABLE public.templates;
       public         heap    postgres    false    5            �            1259    49221    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    5    218            =           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    219            d           2604    49223    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    201    200            e           2604    49224    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202            f           2604    49225    device_presets id    DEFAULT     x   ALTER TABLE ONLY public.device_presets ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 @   ALTER TABLE public.device_presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    207    204            g           2604    49226    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    206    205            h           2604    49227 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    209    208            i           2604    49228    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    210            j           2604    49229    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    213    212            k           2604    49230 
   presets id    DEFAULT     h   ALTER TABLE ONLY public.presets ALTER COLUMN id SET DEFAULT nextval('public.presets_id_seq'::regclass);
 9   ALTER TABLE public.presets ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214            l           2604    49231    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216            m           2604    49232    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218                      0    49153 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    200   �h                 0    49161    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    202   i                 0    49166    device_presets 
   TABLE DATA           T   COPY public.device_presets (id, template_id, ordered_number, preset_id) FROM stdin;
    public          postgres    false    204   Om                 0    49169    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    205   �q       !          0    49176    devices 
   TABLE DATA           c   COPY public.devices (id, name, company_id, dev_type, family_id, boot, uboot, firmware) FROM stdin;
    public          postgres    false    208    r       #          0    49185    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    210   �r       %          0    49190    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    212   hs       '          0    49198    presets 
   TABLE DATA           C   COPY public.presets (id, device_id, description, role) FROM stdin;
    public          postgres    false    214   �s       )          0    49206 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    216   t       +          0    49214 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    218   =t       >           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    201            ?           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 886, true);
          public          postgres    false    203            @           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 96, true);
          public          postgres    false    206            A           0    0    device_templates_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.device_templates_id_seq', 591, true);
          public          postgres    false    207            B           0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 42, true);
          public          postgres    false    209            C           0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 18, true);
          public          postgres    false    211            D           0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    213            E           0    0    presets_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.presets_id_seq', 20, true);
          public          postgres    false    215            F           0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    217            G           0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 385, true);
          public          postgres    false    219            p           2606    49234    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    200            t           2606    49236    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    202            x           2606    49238 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    205            v           2606    49240 $   device_presets device_templates_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    204            z           2606    49242    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    208            ~           2606    49244    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    210            �           2606    49246    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    210            �           2606    49248    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    212            �           2606    49250    presets presets_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_pkey;
       public            postgres    false    214            �           2606    49252    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    216            �           2606    49254    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    218            r           2606    49256    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    200            |           2606    49258    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    208            �           2606    49260    presets unique_device_role 
   CONSTRAINT     `   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT unique_device_role UNIQUE (device_id, role);
 D   ALTER TABLE ONLY public.presets DROP CONSTRAINT unique_device_role;
       public            postgres    false    214    214            �           2606    49312 !   templates unique_family_role_name 
   CONSTRAINT     m   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_family_role_name UNIQUE (family_id, role, name);
 K   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_family_role_name;
       public            postgres    false    218    218    218            �           2606    49261 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    202    2938    208            �           2606    49266 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    202    2946    212            �           2606    49271 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    2938    205    208            �           2606    49276 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    2952    205    216            �           2606    49281 .   device_presets device_templates_preset_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_preset_id_fkey FOREIGN KEY (preset_id) REFERENCES public.presets(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_preset_id_fkey;
       public          postgres    false    214    2948    204            �           2606    49286 0   device_presets device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_presets
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_presets DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    204    2954    218            �           2606    49291    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    208    200    2928            �           2606    49296    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    2944    210    208            �           2606    49301    presets presets_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.presets
    ADD CONSTRAINT presets_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 H   ALTER TABLE ONLY public.presets DROP CONSTRAINT presets_device_id_fkey;
       public          postgres    false    214    208    2938            �           2606    49306 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    210    218    2944               '   x�3〉�H��21�t�)I��21�t,*MJ����� ���         '  x�}�A��6����)|�8bw�ݺK6N0�����#�V,mY�)~�z9m�,_�������~�}�x�������s�L�F�*t�PaNN¥�E�*L�Ra^*���D8I5F.�H.�J.�L.�N.�P.�R.�T.�V!���V�U��	��V�UH+�*��a�ʰ
ieX��2��z�'���
Y�*d��T�Z�����P!+�S�,t.�Ι*䕘%x%�&�hI��ϒH]�%��>K2u}�t��,	��YR��$U�gI��ϒV]���V)��>)��>)��>)��>)��>)��>)���V�UJ+Ǫ��cU�|X��r�JZ9V%���V�UI+Ǫ��cU�*�*iX]�*���U`u�_*�.iX]�*���U`uI�����������������|=�~��|��X|m�հ�_"4¡B��[C����p�
�Ta.a��",�p�j"�B�-��Hl+���
�Ķ�B:�-��Pl+���
IŶ�BZ�-��Vlk��	�)��֔Vlk~Z��y�=�}=�q�cS�(G���
�p���LN�R�"�T�Gک�"*�M"���#�F�(M"Q�4�D��$5J�N�(MBQ�t)E��%5J�V�(]ZQ�t�>a�Ҋ�K+j��i%k�^y�}=���C�����Qo����{އL�[�>�9S�����Cގ�{�a��>,¡�$�I���4�FuJ$jT�T�FuJ&jT�t�FuJ(jTCJQ���ՐVԨ���F5���ՐVԨ���F5���ҊCJi�!�LZqH)�VRʤ��2i�!�LZqH)���ʤ��2i�!�LZqH)�VRʥ��ri�!�\ZqH)�VRʥ��ri�!�\�Ra�ҊCJ���R.�8�TH+)�Vr[����5�?�:�!g�|�F�����?�������ח�wm�{�܌�<����ڌ#���}K�T��(�zǯ/ij��}=s���b�6�����m���˘�8���0�q��/`n�<_���y��t��Ӓ�n�����v��8w+�)���It#�ڌ���6�չ���f���8D�q�*6��܌CTk������q�]��         p  x�E�I��0��c&D,\���Ǡ�L��@�m1MPPu��x�?}�X���c���Q�O��O
���}�`�;뙂U��g	6a�K诨��M$��"Y�Ic�H{�$��H&[&]*[*�.���^�\���b&���H."�X��bC$�"��������r�rq�t��\�\\.]..�.�K��˥������@���7�}o~���j^�e]���Vױ�΅�~W��F��W��ū�DW�U�Tc����"T'�T�E˓5V����R�uc�F+kgUc�쪱n�j��Z-l�u��6��R@�ZJ�k)��%~y�k-��ѳVw���X�]��W��W�e���N�Q{\�}j����X�����V����U���u-V6�u]�z0YC7'�d�Y��;�t�p�\{�.>���Op���?�~���@�����`��h0e`4�20,��KF�%�A���|CF̜:>u���o�Q��v�^��F���u�K�>X����n�u�ڬ��Yo��7~A
:a�0NX� lWG�ʲsyt���5 �5 е��������������h`20��&�^�?4�+7����D0�k���h�uMQ�MQ�MQ�MQ�MQ�MQ�MQ�MQ�Mt�K���rq��\\.)�K���r���5��[7r���rq��\\.)�K�%^Η!��0C.�!�1C.�;`<C.��@��D����� ���pn¹C �����~����@�Hyi��@�'0��	�}h�'0��	$;���'0��R��@'0��	�ui�� ��	�~�N` �	$���1q��qi��@Z'0��	�������Σ��c�rY:&A���-������0 7c n� ܜ�I�e�������/q����R���/y�������E�K �/����r�K"����мy�n"�I��{S	��\��L@~�	(n:}��%ЗQ@��>�~�«��m|k���T=�! � ����/A����P|}g�S\��!���{�pA�G���	��m])"�K�~)�$������B��(��]��[��Y�����������q         A   x����PB���ID?���_G������h*�P����	>��m����Iۘ�����w�r4      !   �   x��P=�0�����R&�&�Fw&(��P��|[��X1Ʀ��޽��p�2j`���d&e��㞸l�B�1F�r8�ő뉍R �z)��*p��I@C4�2���c�)�jb2��C�wA<R2b��;��L��t���:P)��
Z<i5G���9ڢw�2����~��n��\���|-㲹�~�p4����"B< ̑��      #   `   x�ˡ�0EQ�~[��K2�a�`s8L�{x3'y����X�|i�͈�(�2�(��(1a�?��qč�����j��\�z=�x��tND�
�"R      %   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      '   C   x�3�42���LI,I�2�r2r3������.C��9\��1�Vgh�il�%�r�� rb���� 61�      )   '   x�3�t���2��())�2����2�,.������� s��      +     x��ZYs9~��֯�8sr<�l���Q)W������@�+�}u�x.v�&��F�O_��[-�JK�д�[���	���)20p��|�&��e�ӻ�w�B���E��G��;�G�w�M�\ "ӄ�T�'�f3l�HL]��2M�@OQ� 5&��--
�?�$~h�A�����Δ���1	��W�렋j��Mڰ�ڶkb�8�N�x)�S+*$�5���7'�A��O�0D^�Z��l�r���9YeΪ$�s�~�ݓ$-瓶<�:I�J>���cPV�)��c�'��:�! ��^y�`7oM�K���;)��+��T�U��=9���gP����l*y@N;A[�:�OOEY��:����?Y�˲�A����xI]V�Uy�p9�"*���^UL��wr���B9�s�/�,,�g*�*��ڟHE�LU�H��;:�:!+��G>m@�h��yW�+e��}�؏o\!�Wh��õmסe�ݐ`(]��<�҅F]��[`�!Ǳ�����'�1
K/QS�жHB�@����)%b�E��dch/dږ=+�7!v��旇~g��o_ˉܟ^�F޵���BϷ���0��,t�c#l��#�ՇW�����Y���胧`��>R�>�
~!4�>,��qe�B��E�<�Ȉܾ������;&e K"<��g�?Il�v�J�f#/
љ��ft�<�ʨm�Ǩ���c,�]X�z��/�����������4.�V�uU3t���TU��C�=$�Xt�Y����"�	w��y�!��9%>��X�Wh?��>�N�{�ey��7�)k�%���Q��O��M{ ��n5^��7���\������y�=i��-Z�rsu39�j��x]"FE�(�
�RR�w�noX>�*m�5t���`R��@p|����D���	^�Ţ�[��l�j�@��~V&���6��o݄�&X}��&��;��ǃlXbc�"CWۺ x�"-B�����5�݃��m�>O��k4��2��t�g�X9-�*Tt��}�zc�8��	�U�@դ�e�\`�}����l?��ɜ'U�&�xbHF�9[*b�e�W8&�	�v埏�8}���,T���hJ@���2�L;k�{X��U<�30=XO�7	g���+�"���݀0���;r��?vz�����Ͱ�{C���oz_�H� ·�"43��The �����K(��J�m9�-����*�'�
��kP��F+4�}��7��ͱ=��t�7��W\v9�Y����
	���j���77���WM�2V�������?��>/�a�7��g\][�)��)�|�p����/[��yA���\��\���\�����	���+*����k�f�����+�"C��ˡ�N5�Y����Ґ��næ���P4�՞��w���=)(�%-���v*x�7��V*�rZƋ7ۅ���,�ySq9ߌ-%��~���j`��zF�ҳ�AV��zT3J�r��ǯ��r�u��^��\�\�s�n�u��B� ֧w#P��v�]9;�ũ�D�H8��N�(^�x2�kO�x�#�5�ԆTp ��g�@x�oSW8?�MS�3������^��v8���Uq�����p�����i�%>C��o����&�?[$N>)�|*�ТQ
�heD��{�ȡm���C2�9yb3q2�q�i
�&����o�5O���U,P6%�����pdxA�T�Pi�36K�@���/G��!94J�F/ik����S����C1����0�WJWF�lAR��?�
�q.t�[ȅ���?����8%��2�B�EC�[��{U*7�Tjyi{1m���vw0�8�d�j⨒)�rE$!�����`0�埨?�l�>��F�xB^���`.��=l ��%d���%t�Y��	�;9#�ߡ��~��W�����"f�w|���G�#$�T�*��b��+�B/��^f��-��jU������*\�����Y�h\������'���]�������     