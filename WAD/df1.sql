/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80020
 Source Host           : localhost:3306
 Source Schema         : df1

 Target Server Type    : MySQL
 Target Server Version : 80020
 File Encoding         : 65001

 Date: 03/01/2022 21:09:26
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for claim
-- ----------------------------
DROP TABLE IF EXISTS `claim`;
CREATE TABLE `claim`  (
  `claim_id` int(0) NOT NULL AUTO_INCREMENT,
  `claim_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `topic_id` int(0) NULL DEFAULT NULL,
  `claim_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `post_time` datetime(0) NULL DEFAULT NULL,
  `user_id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`claim_id`) USING BTREE,
  INDEX `topic_id`(`topic_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_claim_claim_title`(`claim_title`) USING BTREE,
  CONSTRAINT `claim_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`topic_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `claim_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of claim
-- ----------------------------
INSERT INTO `claim` VALUES (1, 'claim1', 1, 'Claim 1 is about claim1.', '2022-01-02 03:18:48', 'Esther');
INSERT INTO `claim` VALUES (2, 'claim2', 2, 'Claim 2 is about claim2.', '2022-01-02 03:18:48', 'Esther');
INSERT INTO `claim` VALUES (5, 'claim3', 1, 'claim3', '2022-01-02 14:57:39', 'admin');
INSERT INTO `claim` VALUES (6, '1', 1, '1', '2022-01-02 14:57:39', 'admin');
INSERT INTO `claim` VALUES (7, 'asd', 1, 'asd', '2022-01-02 14:57:39', 'admin');
INSERT INTO `claim` VALUES (8, '333', 1, '33333', '2022-01-02 14:57:39', 'admin');

-- ----------------------------
-- Table structure for claim_claim
-- ----------------------------
DROP TABLE IF EXISTS `claim_claim`;
CREATE TABLE `claim_claim`  (
  `claim_id` int(0) NOT NULL,
  `claim_id_` int(0) NULL DEFAULT NULL,
  `relation_cc` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`claim_id`) USING BTREE,
  INDEX `claim_id_`(`claim_id_`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of claim_claim
-- ----------------------------
INSERT INTO `claim_claim` VALUES (8, 1, 'Opposed');
INSERT INTO `claim_claim` VALUES (9, 5, 'Opposed');

-- ----------------------------
-- Table structure for reply
-- ----------------------------
DROP TABLE IF EXISTS `reply`;
CREATE TABLE `reply`  (
  `reply_id` int(0) NOT NULL AUTO_INCREMENT,
  `claim_id` int(0) NULL DEFAULT NULL,
  `reply_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `post_time` datetime(0) NULL DEFAULT NULL,
  `user_id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `rereply_id` int(0) NULL DEFAULT NULL,
  PRIMARY KEY (`reply_id`) USING BTREE,
  INDEX `claim_id`(`claim_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `rereply_id`(`rereply_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reply
-- ----------------------------
INSERT INTO `reply` VALUES (46, 1, 'asdas', '2022-01-03 20:53:07', 'admin', NULL);
INSERT INTO `reply` VALUES (47, 1, 'asd', '2022-01-03 20:53:07', 'admin', 46);

-- ----------------------------
-- Table structure for reply_claim
-- ----------------------------
DROP TABLE IF EXISTS `reply_claim`;
CREATE TABLE `reply_claim`  (
  `reply_id` int(0) NOT NULL,
  `claim_id` int(0) NULL DEFAULT NULL,
  `relation_rc` varchar(19) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`reply_id`) USING BTREE,
  INDEX `claim_id`(`claim_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reply_claim
-- ----------------------------
INSERT INTO `reply_claim` VALUES (46, 1, 'clarification');

-- ----------------------------
-- Table structure for reply_reply
-- ----------------------------
DROP TABLE IF EXISTS `reply_reply`;
CREATE TABLE `reply_reply`  (
  `reply_id` int(0) NOT NULL,
  `reply_id_` int(0) NULL DEFAULT NULL,
  `relation_rr` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`reply_id`) USING BTREE,
  INDEX `reply_id_`(`reply_id_`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reply_reply
-- ----------------------------
INSERT INTO `reply_reply` VALUES (48, 46, 'support');

-- ----------------------------
-- Table structure for topic
-- ----------------------------
DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic`  (
  `topic_id` int(0) NOT NULL AUTO_INCREMENT,
  `topic_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `topic_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `post_time` datetime(0) NULL DEFAULT NULL,
  `user_id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`topic_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_topic_topic_title`(`topic_title`) USING BTREE,
  CONSTRAINT `topic_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of topic
-- ----------------------------
INSERT INTO `topic` VALUES (1, 'Topic1', 'This is topic 1. Topic 1 is a good topic.', '2022-01-02 03:18:48', 'Esther');
INSERT INTO `topic` VALUES (2, 'Topic2', 'This is topic 2. Topic 2 is a good topic, but is different from topic 1.', '2022-01-02 03:18:48', 'Esther');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_password` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'Esther', '123456');
INSERT INTO `user` VALUES (7, 'admin', 'admin');

SET FOREIGN_KEY_CHECKS = 1;
