PGDMP       $                |            device_registry #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) #   16.6 (Ubuntu 16.6-0ubuntu0.24.04.1) d    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16846    device_registry    DATABASE     {   CREATE DATABASE device_registry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE device_registry;
                postgres    false            �            1259    16847 	   companies    TABLE     `   CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.companies;
       public         heap    postgres    false            �            1259    16852    companies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.companies_id_seq;
       public          postgres    false    215            �           0    0    companies_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;
          public          postgres    false    216            �            1259    16853    device_firmwares    TABLE     �   CREATE TABLE public.device_firmwares (
    id integer NOT NULL,
    device_id integer NOT NULL,
    firmware_id integer NOT NULL
);
 $   DROP TABLE public.device_firmwares;
       public         heap    postgres    false            �            1259    16856    device_firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_firmwares_id_seq;
       public          postgres    false    217            �           0    0    device_firmwares_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_firmwares_id_seq OWNED BY public.device_firmwares.id;
          public          postgres    false    218            �            1259    16857    device_ports    TABLE     �   CREATE TABLE public.device_ports (
    id integer NOT NULL,
    device_id integer NOT NULL,
    port_id integer NOT NULL,
    interface character varying(255) NOT NULL
);
     DROP TABLE public.device_ports;
       public         heap    postgres    false            �            1259    16860    device_ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.device_ports_id_seq;
       public          postgres    false    219            �           0    0    device_ports_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.device_ports_id_seq OWNED BY public.device_ports.id;
          public          postgres    false    220            �            1259    16861    device_protocols    TABLE     �   CREATE TABLE public.device_protocols (
    id integer NOT NULL,
    device_id integer NOT NULL,
    protocol_id integer NOT NULL
);
 $   DROP TABLE public.device_protocols;
       public         heap    postgres    false            �            1259    16864    device_protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_protocols_id_seq;
       public          postgres    false    221            �           0    0    device_protocols_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_protocols_id_seq OWNED BY public.device_protocols.id;
          public          postgres    false    222            �            1259    16865    device_templates    TABLE     �   CREATE TABLE public.device_templates (
    id integer NOT NULL,
    device_id integer NOT NULL,
    template_id integer NOT NULL,
    ordered_number integer NOT NULL,
    preset character varying(255) NOT NULL
);
 $   DROP TABLE public.device_templates;
       public         heap    postgres    false            �            1259    16868    device_templates_id_seq    SEQUENCE     �   CREATE SEQUENCE public.device_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.device_templates_id_seq;
       public          postgres    false    223            �           0    0    device_templates_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.device_templates_id_seq OWNED BY public.device_templates.id;
          public          postgres    false    224            �            1259    16869    devices    TABLE     Z  CREATE TABLE public.devices (
    id integer NOT NULL,
    name character varying NOT NULL,
    company_id integer NOT NULL,
    dev_type character varying NOT NULL,
    family_id integer NOT NULL,
    CONSTRAINT check_dev_type CHECK (((dev_type)::text = ANY (ARRAY[('router'::character varying)::text, ('switch'::character varying)::text])))
);
    DROP TABLE public.devices;
       public         heap    postgres    false            �            1259    16875    devices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.devices_id_seq;
       public          postgres    false    225            �           0    0    devices_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;
          public          postgres    false    226            �            1259    16876    families    TABLE     d   CREATE TABLE public.families (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.families;
       public         heap    postgres    false            �            1259    16879    families_id_seq    SEQUENCE     �   CREATE SEQUENCE public.families_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.families_id_seq;
       public          postgres    false    227            �           0    0    families_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.families_id_seq OWNED BY public.families.id;
          public          postgres    false    228            �            1259    16880 	   firmwares    TABLE     �  CREATE TABLE public.firmwares (
    id integer NOT NULL,
    name character varying NOT NULL,
    full_path character varying NOT NULL,
    type character varying NOT NULL,
    CONSTRAINT firmwares_firmware_type_check CHECK (((type)::text = ANY (ARRAY[('primary_bootloader'::character varying)::text, ('secondary_bootloader'::character varying)::text, ('firmware'::character varying)::text])))
);
    DROP TABLE public.firmwares;
       public         heap    postgres    false            �            1259    16886    firmwares_id_seq    SEQUENCE     �   CREATE SEQUENCE public.firmwares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.firmwares_id_seq;
       public          postgres    false    229            �           0    0    firmwares_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.firmwares_id_seq OWNED BY public.firmwares.id;
          public          postgres    false    230            �            1259    16887    ports    TABLE     �   CREATE TABLE public.ports (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    material character varying(255),
    speed integer NOT NULL
);
    DROP TABLE public.ports;
       public         heap    postgres    false            �            1259    16892    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public          postgres    false    231            �           0    0    ports_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.id;
          public          postgres    false    232            �            1259    16893 	   protocols    TABLE     `   CREATE TABLE public.protocols (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.protocols;
       public         heap    postgres    false            �            1259    16898    protocols_id_seq    SEQUENCE     �   CREATE SEQUENCE public.protocols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.protocols_id_seq;
       public          postgres    false    233            �           0    0    protocols_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.protocols_id_seq OWNED BY public.protocols.id;
          public          postgres    false    234            �            1259    16899 	   templates    TABLE     �  CREATE TABLE public.templates (
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
       public         heap    postgres    false            �            1259    16906    template_pieces_id_seq    SEQUENCE     �   CREATE SEQUENCE public.template_pieces_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.template_pieces_id_seq;
       public          postgres    false    235            �           0    0    template_pieces_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.template_pieces_id_seq OWNED BY public.templates.id;
          public          postgres    false    236                       2604    16907    companies id    DEFAULT     l   ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);
 ;   ALTER TABLE public.companies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215                       2604    16908    device_firmwares id    DEFAULT     z   ALTER TABLE ONLY public.device_firmwares ALTER COLUMN id SET DEFAULT nextval('public.device_firmwares_id_seq'::regclass);
 B   ALTER TABLE public.device_firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217                       2604    16909    device_ports id    DEFAULT     r   ALTER TABLE ONLY public.device_ports ALTER COLUMN id SET DEFAULT nextval('public.device_ports_id_seq'::regclass);
 >   ALTER TABLE public.device_ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219                       2604    16910    device_protocols id    DEFAULT     z   ALTER TABLE ONLY public.device_protocols ALTER COLUMN id SET DEFAULT nextval('public.device_protocols_id_seq'::regclass);
 B   ALTER TABLE public.device_protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    221            	           2604    16911    device_templates id    DEFAULT     z   ALTER TABLE ONLY public.device_templates ALTER COLUMN id SET DEFAULT nextval('public.device_templates_id_seq'::regclass);
 B   ALTER TABLE public.device_templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    223            
           2604    16912 
   devices id    DEFAULT     h   ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);
 9   ALTER TABLE public.devices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    225                       2604    16913    families id    DEFAULT     j   ALTER TABLE ONLY public.families ALTER COLUMN id SET DEFAULT nextval('public.families_id_seq'::regclass);
 :   ALTER TABLE public.families ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227                       2604    16914    firmwares id    DEFAULT     l   ALTER TABLE ONLY public.firmwares ALTER COLUMN id SET DEFAULT nextval('public.firmwares_id_seq'::regclass);
 ;   ALTER TABLE public.firmwares ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229                       2604    16915    ports id    DEFAULT     d   ALTER TABLE ONLY public.ports ALTER COLUMN id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 7   ALTER TABLE public.ports ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    231                       2604    16916    protocols id    DEFAULT     l   ALTER TABLE ONLY public.protocols ALTER COLUMN id SET DEFAULT nextval('public.protocols_id_seq'::regclass);
 ;   ALTER TABLE public.protocols ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    233                       2604    16917    templates id    DEFAULT     r   ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.template_pieces_id_seq'::regclass);
 ;   ALTER TABLE public.templates ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    236    235            �          0    16847 	   companies 
   TABLE DATA           -   COPY public.companies (id, name) FROM stdin;
    public          postgres    false    215   x       �          0    16853    device_firmwares 
   TABLE DATA           F   COPY public.device_firmwares (id, device_id, firmware_id) FROM stdin;
    public          postgres    false    217   ;x       �          0    16857    device_ports 
   TABLE DATA           I   COPY public.device_ports (id, device_id, port_id, interface) FROM stdin;
    public          postgres    false    219   Xx       �          0    16861    device_protocols 
   TABLE DATA           F   COPY public.device_protocols (id, device_id, protocol_id) FROM stdin;
    public          postgres    false    221   y       �          0    16865    device_templates 
   TABLE DATA           ^   COPY public.device_templates (id, device_id, template_id, ordered_number, preset) FROM stdin;
    public          postgres    false    223   @y       �          0    16869    devices 
   TABLE DATA           L   COPY public.devices (id, name, company_id, dev_type, family_id) FROM stdin;
    public          postgres    false    225   ]y       �          0    16876    families 
   TABLE DATA           ,   COPY public.families (id, name) FROM stdin;
    public          postgres    false    227   �y       �          0    16880 	   firmwares 
   TABLE DATA           >   COPY public.firmwares (id, name, full_path, type) FROM stdin;
    public          postgres    false    229   �y       �          0    16887    ports 
   TABLE DATA           :   COPY public.ports (id, name, material, speed) FROM stdin;
    public          postgres    false    231   �z       �          0    16893 	   protocols 
   TABLE DATA           -   COPY public.protocols (id, name) FROM stdin;
    public          postgres    false    233   {       �          0    16899 	   templates 
   TABLE DATA           J   COPY public.templates (id, name, type, role, text, family_id) FROM stdin;
    public          postgres    false    235   S{       �           0    0    companies_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.companies_id_seq', 44, true);
          public          postgres    false    216            �           0    0    device_firmwares_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_firmwares_id_seq', 32, true);
          public          postgres    false    218            �           0    0    device_ports_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.device_ports_id_seq', 407, true);
          public          postgres    false    220            �           0    0    device_protocols_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_protocols_id_seq', 60, true);
          public          postgres    false    222            �           0    0    device_templates_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.device_templates_id_seq', 27, true);
          public          postgres    false    224                        0    0    devices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.devices_id_seq', 27, true);
          public          postgres    false    226                       0    0    families_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.families_id_seq', 16, true);
          public          postgres    false    228                       0    0    firmwares_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.firmwares_id_seq', 34, true);
          public          postgres    false    230                       0    0    ports_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.ports_id_seq', 4, true);
          public          postgres    false    232                       0    0    protocols_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.protocols_id_seq', 8, true);
          public          postgres    false    234                       0    0    template_pieces_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.template_pieces_id_seq', 355, true);
          public          postgres    false    236                       2606    16919    companies companies_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.companies DROP CONSTRAINT companies_pkey;
       public            postgres    false    215                       2606    16921 &   device_firmwares device_firmwares_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_pkey;
       public            postgres    false    217                       2606    16923    device_ports device_ports_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_pkey;
       public            postgres    false    219                       2606    16925 &   device_protocols device_protocols_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_pkey;
       public            postgres    false    221            !           2606    16927 &   device_templates device_templates_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.device_templates
    ADD CONSTRAINT device_templates_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.device_templates DROP CONSTRAINT device_templates_pkey;
       public            postgres    false    223            %           2606    16929    devices devices_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_pkey;
       public            postgres    false    225            )           2606    16931    families families_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.families DROP CONSTRAINT families_name_key;
       public            postgres    false    227            +           2606    16933    families families_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.families
    ADD CONSTRAINT families_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.families DROP CONSTRAINT families_pkey;
       public            postgres    false    227            -           2606    16935 !   firmwares firmwares_full_path_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_full_path_key UNIQUE (full_path);
 K   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_full_path_key;
       public            postgres    false    229            /           2606    16937    firmwares firmwares_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT firmwares_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT firmwares_pkey;
       public            postgres    false    229            3           2606    16939    ports ports_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public            postgres    false    231            5           2606    16941    protocols protocols_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.protocols
    ADD CONSTRAINT protocols_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.protocols DROP CONSTRAINT protocols_pkey;
       public            postgres    false    233            7           2606    16943    templates template_pieces_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_pkey;
       public            postgres    false    235                       2606    16945    companies unique_company_name 
   CONSTRAINT     X   ALTER TABLE ONLY public.companies
    ADD CONSTRAINT unique_company_name UNIQUE (name);
 G   ALTER TABLE ONLY public.companies DROP CONSTRAINT unique_company_name;
       public            postgres    false    215                       2606    16947 '   device_firmwares unique_device_firmware 
   CONSTRAINT     t   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT unique_device_firmware UNIQUE (device_id, firmware_id);
 Q   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT unique_device_firmware;
       public            postgres    false    217    217            '           2606    16949    devices unique_device_name 
   CONSTRAINT     U   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT unique_device_name UNIQUE (name);
 D   ALTER TABLE ONLY public.devices DROP CONSTRAINT unique_device_name;
       public            postgres    false    225            1           2606    16951    firmwares unique_firmware_name 
   CONSTRAINT     Y   ALTER TABLE ONLY public.firmwares
    ADD CONSTRAINT unique_firmware_name UNIQUE (name);
 H   ALTER TABLE ONLY public.firmwares DROP CONSTRAINT unique_firmware_name;
       public            postgres    false    229            #           2606    16953 *   device_templates unique_ordered_num_preset 
   CONSTRAINT     w   ALTER TABLE ONLY public.device_templates
    ADD CONSTRAINT unique_ordered_num_preset UNIQUE (ordered_number, preset);
 T   ALTER TABLE ONLY public.device_templates DROP CONSTRAINT unique_ordered_num_preset;
       public            postgres    false    223    223            9           2606    16955    templates unique_template_row 
   CONSTRAINT     u   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT unique_template_row UNIQUE (name, type, role, text, family_id);
 G   ALTER TABLE ONLY public.templates DROP CONSTRAINT unique_template_row;
       public            postgres    false    235    235    235    235    235            :           2606    16956 0   device_firmwares device_firmwares_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_device_id_fkey;
       public          postgres    false    217    225    3365            ;           2606    16961 2   device_firmwares device_firmwares_firmware_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_firmwares
    ADD CONSTRAINT device_firmwares_firmware_id_fkey FOREIGN KEY (firmware_id) REFERENCES public.firmwares(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_firmwares DROP CONSTRAINT device_firmwares_firmware_id_fkey;
       public          postgres    false    3375    229    217            <           2606    16966 (   device_ports device_ports_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_device_id_fkey;
       public          postgres    false    219    225    3365            =           2606    16971 &   device_ports device_ports_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_ports
    ADD CONSTRAINT device_ports_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.device_ports DROP CONSTRAINT device_ports_port_id_fkey;
       public          postgres    false    3379    219    231            >           2606    16976 0   device_protocols device_protocols_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_device_id_fkey;
       public          postgres    false    221    225    3365            ?           2606    16981 2   device_protocols device_protocols_protocol_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_protocols
    ADD CONSTRAINT device_protocols_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocols(id) ON DELETE CASCADE;
 \   ALTER TABLE ONLY public.device_protocols DROP CONSTRAINT device_protocols_protocol_id_fkey;
       public          postgres    false    233    3381    221            @           2606    16986 0   device_templates device_templates_device_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_templates
    ADD CONSTRAINT device_templates_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);
 Z   ALTER TABLE ONLY public.device_templates DROP CONSTRAINT device_templates_device_id_fkey;
       public          postgres    false    223    225    3365            A           2606    16991 2   device_templates device_templates_template_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.device_templates
    ADD CONSTRAINT device_templates_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.templates(id);
 \   ALTER TABLE ONLY public.device_templates DROP CONSTRAINT device_templates_template_id_fkey;
       public          postgres    false    3383    235    223            B           2606    16996    devices devices_company_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.devices DROP CONSTRAINT devices_company_id_fkey;
       public          postgres    false    215    225    3349            C           2606    17001    devices fk_family    FK CONSTRAINT     u   ALTER TABLE ONLY public.devices
    ADD CONSTRAINT fk_family FOREIGN KEY (family_id) REFERENCES public.families(id);
 ;   ALTER TABLE ONLY public.devices DROP CONSTRAINT fk_family;
       public          postgres    false    225    227    3371            D           2606    17006 (   templates template_pieces_family_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.templates
    ADD CONSTRAINT template_pieces_family_id_fkey FOREIGN KEY (family_id) REFERENCES public.families(id);
 R   ALTER TABLE ONLY public.templates DROP CONSTRAINT template_pieces_family_id_fkey;
       public          postgres    false    227    235    3371            �   '   x�3〉�H��21�t�)I��21�t,*MJ����� ���      �      x������ � �      �   �   x�}�1�0D��{
N �]���%HVH���bBͤ~�H_�='���mߞ�}���c�[~d�h�X`eX��a.`g؁�0ăR$
���6RD
IQ)h%E�����vR�
JQ*h)E���4�d��2��2��?��2��ZY���w�녟�������]ֻ�|��      �      x�3��42�4�23 Ѧ\1z\\\ "��      �      x������ � �      �   +   x�32��M-6212�41�,.�,I���22�
[���qqq NB[      �   K   x�ʱ�0C�Cl�N� �T���ܼ;��u<���ٌ�bfB���Ƣ,�b��26�.5~�}�)�� ~O��      �   �   x�����@Ek�_���j�-�MȪY�̂��
0�Z��='wf�Nl@���)��WK��2�W�� \í�{[��c��]�j@~v����!��|��1�K�
�D��۠�2T
�i�Y7�b��=AU���2��y�׭F�\s�u�~JԺ�k-5B�n�0?���+4S�]�Qmϛk8CO-�O1�L}~!��      �   ;   x�3�4400�M*(VH�LJ-ℐ A.#0�]Ҁ�I69�� (� �&�1��b���� g!!�      �   '   x�3�t���2��())�2����2�,.������� s��      �   !  x��X[o�H~���i���-�WZ����
!hRU���`��ul��(�}���6�Ҩ��؞9�|��9��Xk��Ŀ��|�E�����O�x~9�^�o�t��w �w��D�4`fp�=L����slÙ�<�l���3a�Eh2����ا#b�؃6�؉jܦ6����!�hF��ÚZ���
���Y�8
������-��j�T���6�H ��ȇR��� �]�3��f9��!��Z�7q��;U��ɶ�+J9g������r�$pɋ䬕s�GP킲^N�����"9i���� L2�֯>����	���b��c���<�F����'_����7��\+�	9�jl��X=	�<��n�{�+ �?U�+��'ѫx���K���R�N1�TŬ�}'��8���I�I_~��E{*ජ��?Q����j�!��n����0Q6���ɾ�Y)�7��{��&8E��8��ﺾ��.H�8�P���]�J�`�i��-0��o2����*E��%�El,���n��E1�䄩Ab�!Cw"�%P�}jC�YtDL�����D\�gC�|�~~����}Jf��U�� �B�U6�H;�t�G��3o��pb^�&y��3�9�=
�͎t�d�4p�"� ��)�"��Jܾ�����{6c�*2L]�B�[��,6^�y�È�\$��"v�)ڄT�Y�e�5�,��y���K`|�|�M��$UP��$谸�F#ժhe��;J5�T^��JX�V1��+b��X	��5V��R�J��R��&.�PD�B>�f-=H��Ã[$)+�jє��LS�8���L������863d���ILn�^��^��c8ô[����d�G����j4F��{݁fh�xVW���5�s��l�l��)	�C�,N������)K�+�Lى�)���|4�h�vt!� ��E�R6n�ykb�e�"2��P�o�"v���a>b�#����0]�%š\IV��Z^���ޜw���k���Z}��r�����"�D��(D+�I�!ˠ��ҟهʧ����~��F&��2Im�|h��x��X�e�J~,��1u3]di'�VZ��UېDx�%Y䕠�4+��q1��d�&h�6ɂ�d���ꗞܞ�[|����J��i��/+�R̖��y!]�zסj�����P
��#���7�K��iV��XI$�l��|��E�5���C���*G��_?�U�U�,�2�GE�&��}6�����)�`f��/.�5rW^E^����p0M/�#�w����{=|�������ݿ�>��` H���Y� �f[�V@��[��J
���|o3� ��H��V*�"��32y���X�HY�%R\��"�S�p��iIl`pٻ�Ҋ�s�/���Gp��Z���=���QS!�}�<�:��	k�D�;�Aq�wzF�oc�1�|�	��H��ɛGˇ؊E��+T���.� ��p�K�ժ��>�3K,�XAI�~�����V��6��ķ�~pp�?8d�     