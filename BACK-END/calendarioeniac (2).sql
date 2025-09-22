-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 12/09/2025 às 20:45
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `calendarioeniac`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `dados`
--

CREATE TABLE `dados` (
  `id` int(11) NOT NULL,
  `nomeEvento` varchar(255) DEFAULT NULL,
  `dataInicial` varchar(255) DEFAULT NULL,
  `dataFinal` varchar(255) NOT NULL,
  `descricao` text DEFAULT NULL,
  `eventColor` varchar(7) DEFAULT '#054161',
  `imagem_url` varchar(255) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `google_event_id` varchar(255) DEFAULT NULL,
  `semana_do_ano` int(11) DEFAULT NULL,
  `dia_da_semana` int(11) DEFAULT NULL,
  `repetir_anualmente` tinyint(1) DEFAULT 0,
  `evento_tipo` varchar(255) NOT NULL DEFAULT 'externo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `dados`
--

INSERT INTO `dados` (`id`, `nomeEvento`, `dataInicial`, `dataFinal`, `descricao`, `eventColor`, `imagem_url`, `usuario_id`, `google_event_id`, `semana_do_ano`, `dia_da_semana`, `repetir_anualmente`, `evento_tipo`) VALUES
(1, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2026-08-27', '2026-08-27', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(2, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2027-09-02', '2027-09-02', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(3, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2028-08-31', '2028-08-31', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(4, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2029-08-30', '2029-08-30', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(5, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2030-08-29', '2030-08-29', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(6, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2031-08-28', '2031-08-28', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(7, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2032-08-26', '2032-08-26', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(8, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2033-09-01', '2033-09-01', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(9, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2034-08-31', '2034-08-31', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 1, 'aluno, admin'),
(10, 'Exercícios 1, 2, 3 e 4 - 3° Trimestre', '2025-08-28', '2025-08-28', 'Entrega dos Exercícios', '#3788d8', 'bf78b7fa-397e-4ff6-8770-307664ddf38d.svg', 1, NULL, 35, 4, 0, 'aluno, admin'),
(11, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2026-11-07', '2026-11-07', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(12, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2027-11-13', '2027-11-13', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(13, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2028-11-11', '2028-11-11', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(14, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2029-11-10', '2029-11-10', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(15, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2030-11-09', '2030-11-09', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(16, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2031-11-08', '2031-11-08', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(17, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2032-11-06', '2032-11-06', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(18, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2033-11-12', '2033-11-12', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(19, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2034-11-11', '2034-11-11', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 1, 'aluno, admin'),
(20, 'Exercícios 1, 2, 3 e 4 - 4° Trimestre', '2025-11-08', '2025-11-08', 'Entrega dos Exercícios', '#3788d8', '2d4e88c8-330d-4416-8d2b-258ab2057e44.svg', 1, NULL, 45, 6, 0, 'aluno, admin'),
(21, 'Portfólios - 3° Trimestre', '2026-09-03', '2026-09-03', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(22, 'Portfólios - 3° Trimestre', '2027-09-09', '2027-09-09', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(23, 'Portfólios - 3° Trimestre', '2028-09-07', '2028-09-07', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(24, 'Portfólios - 3° Trimestre', '2029-09-06', '2029-09-06', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(25, 'Portfólios - 3° Trimestre', '2030-09-05', '2030-09-05', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(26, 'Portfólios - 3° Trimestre', '2031-09-04', '2031-09-04', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(27, 'Portfólios - 3° Trimestre', '2032-09-02', '2032-09-02', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(28, 'Portfólios - 3° Trimestre', '2033-09-08', '2033-09-08', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(29, 'Portfólios - 3° Trimestre', '2034-09-07', '2034-09-07', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 1, 'aluno, admin'),
(30, 'Portfólios - 3° Trimestre', '2025-09-04', '2025-09-04', 'Entrega dos Portfólios', '#3788d8', '838d7fa9-7d1f-4b9d-bc6a-4158755edab7.svg', 1, NULL, 36, 4, 0, 'aluno, admin'),
(31, 'Portfólios - 4° Trimestre', '2026-11-12', '2026-11-12', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(32, 'Portfólios - 4° Trimestre', '2027-11-18', '2027-11-18', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(33, 'Portfólios - 4° Trimestre', '2028-11-16', '2028-11-16', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(34, 'Portfólios - 4° Trimestre', '2029-11-15', '2029-11-15', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(35, 'Portfólios - 4° Trimestre', '2030-11-14', '2030-11-14', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(36, 'Portfólios - 4° Trimestre', '2031-11-13', '2031-11-13', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(37, 'Portfólios - 4° Trimestre', '2032-11-11', '2032-11-11', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(38, 'Portfólios - 4° Trimestre', '2033-11-17', '2033-11-17', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(39, 'Portfólios - 4° Trimestre', '2034-11-16', '2034-11-16', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 1, 'aluno, admin'),
(40, 'Portfólios - 4° Trimestre', '2025-11-13', '2025-11-13', 'Entrega dos Portfólios', '#3788d8', '45fa6d93-1f15-4e58-947b-38be4500e6e8.svg', 1, NULL, 46, 4, 0, 'aluno, admin'),
(41, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2026-09-25', '2026-09-25', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(42, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2027-10-01', '2027-10-01', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(43, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2028-09-29', '2028-09-29', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(44, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2029-09-28', '2029-09-28', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(45, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2030-09-27', '2030-09-27', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(46, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2031-09-26', '2031-09-26', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(47, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2032-09-24', '2032-09-24', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(48, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2033-09-30', '2033-09-30', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(49, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2034-09-29', '2034-09-29', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 1, 'aluno, admin'),
(50, 'Exercícios 5, 6, 7 e 8 - 3° Trimestre', '2025-09-26', '2025-09-26', 'Entrega dos Exercícios', '#3788d8', '1cc3e3bd-d8ea-4983-8c43-d3eedcd693b6.svg', 1, NULL, 39, 5, 0, 'aluno, admin'),
(51, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2026-12-08', '2026-12-08', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(52, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2027-12-14', '2027-12-14', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(53, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2028-12-12', '2028-12-12', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(54, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2029-12-11', '2029-12-11', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(55, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2030-12-10', '2030-12-10', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(56, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2031-12-09', '2031-12-09', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(57, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2032-12-07', '2032-12-07', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(58, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2033-12-13', '2033-12-13', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(59, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2034-12-12', '2034-12-12', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(60, 'Exercícios 5, 6, 7 e 8 - 4° Trimestre', '2025-12-09', '2025-12-09', 'Entrega dos Exercícios', '#3788d8', '182f3daa-8e67-4a36-8049-48033e07f2a7.svg', 1, NULL, 50, 2, 0, 'aluno, admin'),
(61, 'Prova 1° Chamada - 3° Trimestre', '2026-09-28', '2026-10-02', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(62, 'Prova 1° Chamada - 3° Trimestre', '2027-10-04', '2027-10-08', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(63, 'Prova 1° Chamada - 3° Trimestre', '2028-10-02', '2028-10-06', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(64, 'Prova 1° Chamada - 3° Trimestre', '2029-10-01', '2029-10-05', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(65, 'Prova 1° Chamada - 3° Trimestre', '2030-09-30', '2030-10-04', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(66, 'Prova 1° Chamada - 3° Trimestre', '2031-09-29', '2031-10-03', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(67, 'Prova 1° Chamada - 3° Trimestre', '2032-09-27', '2032-10-01', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(68, 'Prova 1° Chamada - 3° Trimestre', '2033-10-03', '2033-10-07', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(69, 'Prova 1° Chamada - 3° Trimestre', '2034-10-02', '2034-10-06', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 1, 'aluno, admin'),
(70, 'Prova 1° Chamada - 3° Trimestre', '2025-09-29', '2025-10-03', '1° Chamada de provas', '#3788d8', '4f3410d1-87e1-45bf-86ae-4c50371993c0.svg', 1, NULL, 40, 1, 0, 'aluno, admin'),
(71, 'Prova 1° Chamada - 4° Trimestre', '2026-12-08', '2026-12-14', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(72, 'Prova 1° Chamada - 4° Trimestre', '2027-12-14', '2027-12-20', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(73, 'Prova 1° Chamada - 4° Trimestre', '2028-12-12', '2028-12-18', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(74, 'Prova 1° Chamada - 4° Trimestre', '2029-12-11', '2029-12-17', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(75, 'Prova 1° Chamada - 4° Trimestre', '2030-12-10', '2030-12-16', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(76, 'Prova 1° Chamada - 4° Trimestre', '2031-12-09', '2031-12-15', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(77, 'Prova 1° Chamada - 4° Trimestre', '2032-12-07', '2032-12-13', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(78, 'Prova 1° Chamada - 4° Trimestre', '2033-12-13', '2033-12-19', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(79, 'Prova 1° Chamada - 4° Trimestre', '2034-12-12', '2034-12-18', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 1, 'aluno, admin'),
(80, 'Prova 1° Chamada - 4° Trimestre', '2025-12-09', '2025-12-15', '1° Chamada de provas', '#3788d8', '43589fb3-b828-44b5-9f10-82f2a3d91837.svg', 1, NULL, 50, 2, 0, 'aluno, admin'),
(81, 'Portfólios de Recuperação - 3° Trimestre', '2026-09-30', '2026-09-30', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(82, 'Portfólios de Recuperação - 3° Trimestre', '2027-10-06', '2027-10-06', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(83, 'Portfólios de Recuperação - 3° Trimestre', '2028-10-04', '2028-10-04', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(84, 'Portfólios de Recuperação - 3° Trimestre', '2029-10-03', '2029-10-03', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(85, 'Portfólios de Recuperação - 3° Trimestre', '2030-10-02', '2030-10-02', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(86, 'Portfólios de Recuperação - 3° Trimestre', '2031-10-01', '2031-10-01', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(87, 'Portfólios de Recuperação - 3° Trimestre', '2032-09-29', '2032-09-29', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(88, 'Portfólios de Recuperação - 3° Trimestre', '2033-10-05', '2033-10-05', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(89, 'Portfólios de Recuperação - 3° Trimestre', '2034-10-04', '2034-10-04', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 1, 'aluno, admin'),
(90, 'Portfólios de Recuperação - 3° Trimestre', '2025-10-01', '2025-10-01', 'Entrega dos portfólios de recuperação', '#3788d8', '96d3a52a-ce04-49a6-9caf-34c9a052df21.svg', 1, NULL, 40, 3, 0, 'aluno, admin'),
(91, 'Portfólios de Recuperação - 4° Trimestre', '2026-12-03', '2026-12-03', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(92, 'Portfólios de Recuperação - 4° Trimestre', '2027-12-09', '2027-12-09', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(93, 'Portfólios de Recuperação - 4° Trimestre', '2028-12-07', '2028-12-07', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(94, 'Portfólios de Recuperação - 4° Trimestre', '2029-12-06', '2029-12-06', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(95, 'Portfólios de Recuperação - 4° Trimestre', '2030-12-05', '2030-12-05', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(96, 'Portfólios de Recuperação - 4° Trimestre', '2031-12-04', '2031-12-04', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(97, 'Portfólios de Recuperação - 4° Trimestre', '2032-12-02', '2032-12-02', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(98, 'Portfólios de Recuperação - 4° Trimestre', '2033-12-08', '2033-12-08', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(99, 'Portfólios de Recuperação - 4° Trimestre', '2034-12-07', '2034-12-07', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 1, 'aluno, admin'),
(100, 'Portfólios de Recuperação - 4° Trimestre', '2025-12-04', '2025-12-04', 'Entrega dos Portfólios de recuperação', '#3788d8', '548057e5-0ce8-498a-9df1-e28d60fbe839.svg', 1, NULL, 49, 4, 0, 'aluno, admin'),
(111, 'Prova de Recuperação - 4° Trimestre', '2026-12-16', '2026-12-17', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(112, 'Prova de Recuperação - 4° Trimestre', '2027-12-22', '2027-12-23', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(113, 'Prova de Recuperação - 4° Trimestre', '2028-12-20', '2028-12-21', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(114, 'Prova de Recuperação - 4° Trimestre', '2029-12-19', '2029-12-20', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(115, 'Prova de Recuperação - 4° Trimestre', '2030-12-18', '2030-12-19', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(116, 'Prova de Recuperação - 4° Trimestre', '2031-12-17', '2031-12-18', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(117, 'Prova de Recuperação - 4° Trimestre', '2032-12-15', '2032-12-16', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(118, 'Prova de Recuperação - 4° Trimestre', '2033-12-21', '2033-12-22', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(119, 'Prova de Recuperação - 4° Trimestre', '2034-12-20', '2034-12-21', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 1, 'aluno, admin'),
(120, 'Prova de Recuperação - 4° Trimestre', '2025-12-17', '2025-12-18', 'Provas de recuperação', '#3788d8', '629c111c-e5e6-4900-94d6-e436dae09079.svg', 1, NULL, 51, 3, 0, 'aluno, admin'),
(131, 'Prova de Recuperação - 3° Trimestre', '2026-10-07', '2026-10-08', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(132, 'Prova de Recuperação - 3° Trimestre', '2027-10-13', '2027-10-14', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(133, 'Prova de Recuperação - 3° Trimestre', '2028-10-11', '2028-10-12', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(134, 'Prova de Recuperação - 3° Trimestre', '2029-10-10', '2029-10-11', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(135, 'Prova de Recuperação - 3° Trimestre', '2030-10-09', '2030-10-10', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(136, 'Prova de Recuperação - 3° Trimestre', '2031-10-08', '2031-10-09', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(137, 'Prova de Recuperação - 3° Trimestre', '2032-10-06', '2032-10-07', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(138, 'Prova de Recuperação - 3° Trimestre', '2033-10-12', '2033-10-13', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(139, 'Prova de Recuperação - 3° Trimestre', '2034-10-11', '2034-10-12', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 1, 'aluno, admin'),
(140, 'Prova de Recuperação - 3° Trimestre', '2025-10-08', '2025-10-09', 'Prova de recuperação ', '#3788d8', '24d77f4c-fe8b-45c0-a021-454d1be0f764.svg', 1, NULL, 41, 3, 0, 'aluno, admin'),
(141, 'Prova - 2° Chamada - 3° Trimestre', '2026-10-23', '2026-10-24', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(142, 'Prova - 2° Chamada - 3° Trimestre', '2027-10-29', '2027-10-30', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(143, 'Prova - 2° Chamada - 3° Trimestre', '2028-10-27', '2028-10-28', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(144, 'Prova - 2° Chamada - 3° Trimestre', '2029-10-26', '2029-10-27', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(145, 'Prova - 2° Chamada - 3° Trimestre', '2030-10-25', '2030-10-26', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(146, 'Prova - 2° Chamada - 3° Trimestre', '2031-10-24', '2031-10-25', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(147, 'Prova - 2° Chamada - 3° Trimestre', '2032-10-22', '2032-10-23', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(148, 'Prova - 2° Chamada - 3° Trimestre', '2033-10-28', '2033-10-29', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(149, 'Prova - 2° Chamada - 3° Trimestre', '2034-10-27', '2034-10-28', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 1, 'aluno, admin'),
(150, 'Prova - 2° Chamada - 3° Trimestre', '2025-10-24', '2025-10-25', '2° chamada da prova', '#3788d8', '81f61b18-6f48-4f0f-80e4-01773c66d067.svg', 1, NULL, 43, 5, 0, 'aluno, admin'),
(151, 'Prova - 2° Chamada - 4° Trimestre', '2026-12-18', '2026-12-19', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(152, 'Prova - 2° Chamada - 4° Trimestre', '2027-12-24', '2027-12-25', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(153, 'Prova - 2° Chamada - 4° Trimestre', '2028-12-22', '2028-12-23', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(154, 'Prova - 2° Chamada - 4° Trimestre', '2029-12-21', '2029-12-22', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(155, 'Prova - 2° Chamada - 4° Trimestre', '2030-12-20', '2030-12-21', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(156, 'Prova - 2° Chamada - 4° Trimestre', '2031-12-19', '2031-12-20', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(157, 'Prova - 2° Chamada - 4° Trimestre', '2032-12-17', '2032-12-18', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(158, 'Prova - 2° Chamada - 4° Trimestre', '2033-12-23', '2033-12-24', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(159, 'Prova - 2° Chamada - 4° Trimestre', '2034-12-22', '2034-12-23', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 1, 'aluno, admin'),
(160, 'Prova - 2° Chamada - 4° Trimestre', '2025-12-19', '2025-12-20', 'Prova 2° Chamada', '#3788d8', '6c9b1895-8e37-4f92-98b8-de60ad51b209.svg', 1, NULL, 51, 5, 0, 'aluno, admin');

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'user',
  `tipo_usuario` enum('aluno','externo','admin') NOT NULL DEFAULT 'externo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `senha`, `role`, `tipo_usuario`) VALUES
(1, 'admin', '123admin', 'admin', 'admin'),
(2, 'bruno', 'admin123', 'user', 'aluno'),
(3, 'leonardo', 'admin', 'user', 'aluno'),
(4, 'guilherme', 'senha007', 'user', 'externo'),
(5, 'deivid', 'senha123', 'user', 'externo');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `dados`
--
ALTER TABLE `dados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_usuario_id` (`usuario_id`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `dados`
--
ALTER TABLE `dados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=161;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `dados`
--
ALTER TABLE `dados`
  ADD CONSTRAINT `fk_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;