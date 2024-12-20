PGDMP      
                |            device_registry #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) c    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16685    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false            �            1259    16686 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false            �            1259    16691    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    215            �           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    216            �            1259    16692    device_firmwares    TABLE     �   CREATE TABLE public.device_firmwares (
    id integer NOT NULL,
    device_id integer NOT NULL,
    firmware_id integer NOT NULL
);
 $   DROP TABLE public.device_firmwares;
       public         heap    postgres    false            �            1259    16695    device_firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_firmwares_id_seq;
       public          postgres    false    217            �           0    0    device_firmwares_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_firmwares_id_seq OWNED BY public.device_firmwares.id;
          public          postgres    false    218            �            1259    16696    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    name character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false            �            1259    16699    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    219            �           0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    220            �            1259    16700    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false            �            1259    16703    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    221            �           0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    222            �            1259    16830    device_templates    TABLE     �   CREATE TABLE public.device_templates (
    id integer NOT NULL,
    device_id integer NOT NULL,
    template_id integer NOT NULL,
    order_number integer NOT NULL
);
 $   DROP TABLE public.device_templates;
       public         heap    postgres    false            �            1259    16829    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    236            �           0    0    device_templates_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_templates.id;
          public          postgres    false    235            �            1259    16704    devices    TABLE     Z  CREATE TABLE public.devices (
    id integer NOT NULL,
    name character varying NOT NULL,
    company_id integer NOT NULL,
    dev_type character varying NOT NULL,
    family_id integer NOT NULL,
    CONSTRAINT check_dev_type CHECK (((dev_type)::text = ANY (ARRAY[('router'::character varying)::text, ('switch'::character varying)::text])))
);
    DROP TABLE public.devices;
       public         heap    postgres    false            �            1259    16710    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    223            �           0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    224            �            1259    16711    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false            �            1259    16714    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    225            �           0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    226            �            1259    16715 	   firmwares    TABLE     �  CREATE TABLE public.firmwares (
    id integer NOT NULL,
    name character varying NOT NULL,
    full_path character varying NOT NULL,
    type character varying NOT NULL,
    CONSTRAINT firmwares_firmware_type_check CHECK (((type)::text = ANY (ARRAY[('primary_bootloader'::character varying)::text, ('secondary_bootloader'::character varying)::text, ('firmware'::character varying)::text])))
);
    DROP TABLE public.firmwares;
       public         heap    postgres    false            �            1259    16721    firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.firmwares_id_seq;
       public          postgres    false    227            �           0    0    firmwares_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.firmwares_id_seq OWNED BY public.firmwares.id;
          public          postgres    false    228            �            1259    16722    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false            �            1259    16727    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    229            �           0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    230            �            1259    16728 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false            �            1259    16733    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    231            �           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    232            �            1259    16734 	   templates    TABLE     �   CREATE TABLE public.templates (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    role character varying NOT NULL,
    text text NOT NULL,
    family_id integer NOT NULL
);
    DROP TABLE public.templates;
       public         heap    postgres    false            �            1259    16739    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    233            �           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    234                       2604    16740    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215                       2604    16741    device_firmwares id    DEFAULT     z   ALTER TABLE ONLY public.device_firmwares ALTER COLUMN id SET DEFAULT nextval('public.device_firmwares_id_seq'::regclass);
 B   ALTER TABLE public.device_firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217                       2604    16742    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219                       2604    16743    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    221                       2604    16833    device_templates id    DEFAULT     z   ALTER TABLE ONLY public.device_templates ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 B   ALTER TABLE public.device_templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    235    236    236            	           2604    16744 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223            
           2604    16745    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225                       2604    16746    firmwares id    DEFAULT     l   ALTER TABLE ONLY public.firmwares ALTER COLUMN id SET DEFAULT nextval('public.firmwares_id_seq'::regclass);
 ;   ALTER TABLE public.firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227                       2604    16747    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229                       2604    16748    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231                       2604    16749    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    233            �          0    16686 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    215   ts       �          0    16692    device_firmwares 
   TABLE DATA           F   COPY public.device_firmwares (id, device_id, firmware_id) FROM stdin;
    public          postgres    false    217   �s       �          0    16696    device_ports 
   TABLE DATA           D   COPY public.device_ports (id, device_id, port_id, name) FROM stdin;
    public          postgres    false    219   �s       �          0    16700    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    221   �s       �          0    16830    device_templates 
   TABLE DATA           T   COPY public.device_templates (id, device_id, template_id, order_number) FROM stdin;
    public          postgres    false    236   #t       �          0    16704    devices 
   TABLE DATA           L   COPY public.devices (id, name, company_id, dev_type, family_id) FROM stdin;
    public          postgres    false    223   @t       �          0    16711    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    225   �t       �          0    16715 	   firmwares 
   TABLE DATA           >   COPY public.firmwares (id, name, full_path, type) FROM stdin;
    public          postgres    false    227   �t       �          0    16722    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    229   �u       �          0    16728 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    231   v       �          0    16734 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    233   Ov       �           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 41, true);
          public          postgres    false    216            �           0    0    device_firmwares_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_firmwares_id_seq', 23, true);
          public          postgres    false    218            �           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 293, true);
          public          postgres    false    220            �           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 42, true);
          public          postgres    false    222            �           0    0    device_templates_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_templates_id_seq', 1, false);
          public          postgres    false    235            �           0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 26, true);
          public          postgres    false    224            �           0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 15, true);
          public          postgres    false    226            �           0    0    firmwares_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.firmwares_id_seq', 34, true);
          public          postgres    false    228            �           0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    230                        0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 7, true);
          public          postgres    false    232                       0    0    template_pieces_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.template_pieces_id_seq', 9, true);
          public          postgres    false    234                       2606    16751    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    215                       2606    16753 &   device_firmwares device_firmwares_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_pkey;
       public            postgres    false    217                       2606    16755    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    219                       2606    16757 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    221            5           2606    16835 &   device_templates device_templates_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_templates
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_templates DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    236                       2606    16759    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    223            #           2606    16761    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    225            %           2606    16763    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    225            '           2606    16765 !   firmwares firmwares_full_path_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_full_path_key UNIQUE (full_path);
 K   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_full_path_key;
       public            postgres    false    227            )           2606    16767    firmwares firmwares_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_pkey;
       public            postgres    false    227            -           2606    16769    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    229            /           2606    16771    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    231            1           2606    16773    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    233                       2606    16775    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    215                       2606    16777 '   device_firmwares unique_device_firmware 
   CONSTRAINT     t   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT unique_device_firmware UNIQUE (device_id, firmware_id);
 Q   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT unique_device_firmware;
       public            postgres    false    217    217            !           2606    16779    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    223            +           2606    16781    firmwares unique_firmware_name 
   CONSTRAINT     Y   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT unique_firmware_name UNIQUE (name);
 H   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT unique_firmware_name;
       public            postgres    false    227            3           2606    16783    templates unique_name_type_role 
   CONSTRAINT     f   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_name_type_role UNIQUE (name, type, role);
 I   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_name_type_role;
       public            postgres    false    233    233    233            6           2606    16784 0   device_firmwares device_firmwares_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_device_id_fkey;
       public          postgres    false    3359    223    217            7           2606    16789 2   device_firmwares device_firmwares_firmware_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_firmware_id_fkey FOREIGN KEY (firmware_id) REFERENCES public.firmwares(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_firmware_id_fkey;
       public          postgres    false    3369    217    227            8           2606    16794 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    219    3359    223            9           2606    16799 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    219    229    3373            :           2606    16804 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    221    223    3359            ;           2606    16809 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    231    3375    221            <           2606    16814    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    215    223    3347            ?           2606    16836    device_templates fk_device    FK CONSTRAINT     }   ALTER TABLE ONLY public.device_templates
    ADD CONSTRAINT fk_device FOREIGN KEY (device_id) REFERENCES public.devices(id);
 D   ALTER TABLE ONLY public.device_templates DROP CONSTRAINT fk_device;
       public          postgres    false    236    3359    223            =           2606    16819    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    223    3365    225            >           2606    16824    templates fk_family    FK CONSTRAINT     w   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 =   ALTER TABLE ONLY public.templates DROP CONSTRAINT fk_family;
       public          postgres    false    225    233    3365            @           2606    16841    device_templates fk_template    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_templates
    ADD CONSTRAINT fk_template FOREIGN KEY (template_id) REFERENCES public.templates(id);
 F   ALTER TABLE ONLY public.device_templates DROP CONSTRAINT fk_template;
       public          postgres    false    3377    233    236            �      x�3〉�H��21�t�)I������� F�      �      x������ � �      �   *   x�3�4�42�4�L�LOL�,I-�H-�K-Q0�7������ �S�      �      x�31�42�4�21��\1z\\\ !��      �      x������ � �      �   6   x�32��M-6212�41�,.�,I���22㌪�H�142�4�	�p��qqq dz�      �   Y   x��1� CњF	�
֎�6R�x�/�y3��=�g���&�'�w0�B�IR�
UR֞����#��q���h�c��� =���� ����      �   �   x�����@Ek�_���j�-�MȪY�̂��
0�Z��='wf�Nl@���)��WK��2�W�� \í�{[��c��]�j@~v����!��|��1�K�
�D��۠�2T
�i�Y7�b��=AU���2��y�׭F�\s�u�~JԺ�k-5B�n�0?���+4S�]�Qmϛk8CO-�O1�L}~!��      �   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      �   '   x�3�t���2��())�2����2�,.������� s��      �      x������ � �     