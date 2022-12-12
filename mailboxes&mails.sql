
##### emetteurs

CREATE TABLE `emetteurs` (
  `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) CHARACTER SET utf8mb3 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `emetteurs`
  ADD UNIQUE KEY `nom` (`nom`);

INSERT INTO `emetteurs` (`nom`) VALUES
  ("admin_mailbox");
##### mailboxes

CREATE TABLE `mailboxes` (
  `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  `emetteur_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `mailboxes` (`nom`, `emetteur_id`) VALUES
  ("admin_mailbox", 1);

ALTER TABLE `mailboxes`
  ADD UNIQUE KEY `nom` (`nom`);
ALTER TABLE `mailboxes`
  ADD KEY (`emetteur_id`);

##### mails

CREATE TABLE `mails` (
  `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `read` TINYINT NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb3 NOT NULL,
  `message` LONGTEXT CHARACTER SET utf8mb3 NOT NULL,
  `emetteur_id` int(11) NOT NULL,
  `mailboxe_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `mails` (`read`, `title`, `message`, `emetteur_id`, `mailboxe_id`) VALUES 
  (false, "perpignan", "c'est une magnifique ville (non.)", 1, 1);

ALTER TABLE `mails`
  ADD KEY (`emetteur_id`);
ALTER TABLE `mails`
  ADD KEY (`mailboxe_id`);

#### ajout constraints

ALTER TABLE `mails`
  ADD CONSTRAINT `mails_ibfk_1` FOREIGN KEY (`mailboxe_id`) REFERENCES `mailboxes` (`id`);
ALTER TABLE `mails`
  ADD CONSTRAINT `mails_ibfk_2` FOREIGN KEY (`emetteur_id`) REFERENCES `emetteurs` (`id`);

ALTER TABLE `mailboxes`
  ADD CONSTRAINT `mailboxes_ibfk_1` FOREIGN KEY (`emetteur_id`) REFERENCES `emetteurs` (`id`);