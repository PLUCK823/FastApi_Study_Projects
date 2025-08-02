CREATE TABLE `todolist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `priority` varchar(255) DEFAULT NULL,
  `compeleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_todolist_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 插入10条示例数据
INSERT INTO `todolist` (`title`, `description`, `priority`, `compeleted`) VALUES
('完成项目计划', '制定详细的项目开发计划和时间表', 'high', 0),
('设计数据库模型', '设计并实现todolist应用的数据库结构', 'high', 0),
('实现用户认证', '添加用户注册和登录功能', 'medium', 0),
('创建任务列表页面', '开发前端任务列表展示页面', 'medium', 1),
('添加任务创建功能', '实现创建新任务的功能', 'high', 0),
('实现任务编辑功能', '允许用户编辑现有任务的详情', 'medium', 0),
('添加任务删除功能', '允许用户删除不再需要的任务', 'low', 1),
('实现任务搜索功能', '添加按标题或描述搜索任务的功能', 'low', 0),
('添加任务过滤功能', '允许用户按优先级或完成状态过滤任务', 'medium', 0),
('优化应用性能', '对应用进行性能分析和优化', 'high', 0);