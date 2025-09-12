-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 08/09/2025 às 21:17
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
  `repetir_anualmente` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `dados`
--

INSERT INTO `dados` (`id`, `nomeEvento`, `dataInicial`, `dataFinal`, `descricao`, `eventColor`, `imagem_url`, `usuario_id`, `google_event_id`, `semana_do_ano`, `dia_da_semana`, `repetir_anualmente`) VALUES
(1, 'FERIAS', '2025-09-14 00:00:00', '2025-09-14 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(2, 'FERIAS', '2026-09-13 00:00:00', '2026-09-13 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(3, 'FERIAS', '2027-09-19 00:00:00', '2027-09-19 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(4, 'FERIAS', '2028-09-17 00:00:00', '2028-09-17 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(5, 'FERIAS', '2029-09-16 00:00:00', '2029-09-16 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(6, 'FERIAS', '2030-09-15 00:00:00', '2030-09-15 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(7, 'FERIAS', '2031-09-14 00:00:00', '2031-09-14 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(8, 'FERIAS', '2032-09-12 00:00:00', '2032-09-12 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(9, 'FERIAS', '2033-09-18 00:00:00', '2033-09-18 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(10, 'FERIAS', '2034-09-17 00:00:00', '2034-09-17 00:00:00', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 1),
(11, 'FERIAS', '2025-09-14', '2025-09-14', 'ferias', '#3788d8', NULL, 2, NULL, 37, 7, 0),
(12, 'aula de futebol ENIAC', '2025-09-09 00:00:00', '2025-09-09 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(13, 'aula de futebol ENIAC', '2026-09-08 00:00:00', '2026-09-08 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(14, 'aula de futebol ENIAC', '2027-09-14 00:00:00', '2027-09-14 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(15, 'aula de futebol ENIAC', '2028-09-12 00:00:00', '2028-09-12 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(16, 'aula de futebol ENIAC', '2029-09-11 00:00:00', '2029-09-11 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(17, 'aula de futebol ENIAC', '2030-09-10 00:00:00', '2030-09-10 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(18, 'aula de futebol ENIAC', '2031-09-09 00:00:00', '2031-09-09 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(19, 'aula de futebol ENIAC', '2032-09-07 00:00:00', '2032-09-07 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(20, 'aula de futebol ENIAC', '2033-09-13 00:00:00', '2033-09-13 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(21, 'aula de futebol ENIAC', '2034-09-12 00:00:00', '2034-09-12 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 1),
(22, 'aula de futebol ENIAC', '2025-09-09', '2025-09-09', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '8baaed8b-2ef7-4431-af73-3665ee159914.png', 1, NULL, 37, 2, 0),
(23, 'aula de futebol ENIAC', '2025-09-09 00:00:00', '2025-09-09 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(24, 'aula de futebol ENIAC', '2026-09-08 00:00:00', '2026-09-08 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(25, 'aula de futebol ENIAC', '2027-09-14 00:00:00', '2027-09-14 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(26, 'aula de futebol ENIAC', '2028-09-12 00:00:00', '2028-09-12 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(27, 'aula de futebol ENIAC', '2029-09-11 00:00:00', '2029-09-11 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(28, 'aula de futebol ENIAC', '2030-09-10 00:00:00', '2030-09-10 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(29, 'aula de futebol ENIAC', '2031-09-09 00:00:00', '2031-09-09 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(30, 'aula de futebol ENIAC', '2032-09-07 00:00:00', '2032-09-07 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(31, 'aula de futebol ENIAC', '2033-09-13 00:00:00', '2033-09-13 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(32, 'aula de futebol ENIAC', '2034-09-12 00:00:00', '2034-09-12 00:00:00', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 1),
(33, 'aula de futebol ENIAC', '2025-09-09', '2025-09-09', 'AAAAAAAAAAAAAAAAAAA', '#8cff00', '03a1dcb4-be0f-4c5f-aef6-8d055d9f9002.png', 1, NULL, 37, 2, 0);

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `senha`, `role`) VALUES
(1, 'admin', '123admin', 'admin'),
(2, 'bruno', 'admin123', 'user');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
