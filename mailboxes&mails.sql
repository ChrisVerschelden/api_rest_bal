CREATE TABLE `pays` (
  `id` int(11) NOT NULL,
  `nom` varchar(255) CHARACTER SET utf8mb3 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `pays`
  ADD PRIMARY KEY (`id`);
  ADD UNIQUE KEY `nom` (`nom`);
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
  


INSERT INTO `pays` (`id`, `nom`) VALUES
(1, "france");

ALTER TABLE `regions`
  ADD `pays_id` int(11),
  ADD KEY `pays_id` (`pays_id`);

UPDATE `regions` SET pays_id = 1;

ALTER TABLE `regions`
  ADD CONSTRAINT `regions_ibfk_1` FOREIGN KEY (`pays_id`) REFERENCES `pays` (`id`);


CREATE TABLE `villes` (
  `id` int(11) NOT NULL,
  `code` int(11) NOT NULL,
  `nom` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  `departement_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `villes`
  ADD PRIMARY KEY `id` (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD UNIQUE KEY `nom` (`nom`),
  ADD KEY (`departement_id`);

INSERT INTO `villes` VALUES
(1, 66000, "perpignan", 12);

ALTER TABLE `villes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
  ADD CONSTRAINT `villes_ibfk_1` FOREIGN KEY (`departement_id`) REFERENCES `departements` (`id`);
