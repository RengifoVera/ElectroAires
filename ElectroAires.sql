PGDMP         
                y            ElectroAires    12.1    12.1                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    24885    ElectroAires    DATABASE     �   CREATE DATABASE "ElectroAires" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Spanish_Latin America.1252' LC_CTYPE = 'Spanish_Latin America.1252';
    DROP DATABASE "ElectroAires";
                postgres    false            �            1259    24886    electro    TABLE     �   CREATE TABLE public.electro (
    fecha date,
    marca text,
    tipo_carro text,
    placa character(10) NOT NULL,
    valor numeric,
    arreglo text,
    valor_materiales numeric,
    fecha_ingreso date,
    arreglo_nuevo text
);
    DROP TABLE public.electro;
       public         heap    postgres    false            �
          0    24886    electro 
   TABLE DATA           �   COPY public.electro (fecha, marca, tipo_carro, placa, valor, arreglo, valor_materiales, fecha_ingreso, arreglo_nuevo) FROM stdin;
    public          postgres    false    202   5       
           2606    24893    electro electro_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.electro
    ADD CONSTRAINT electro_pkey PRIMARY KEY (placa);
 >   ALTER TABLE ONLY public.electro DROP CONSTRAINT electro_pkey;
       public            postgres    false    202            �
      x������ � �     