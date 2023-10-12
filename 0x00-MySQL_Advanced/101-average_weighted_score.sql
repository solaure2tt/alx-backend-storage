-- SQL script that creates a stored procedure
-- that computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS U,
        (SELECT U.id, SUM(score * weight) / SUM(weight) AS weight_avg
        FROM users AS U
        JOIN corrections as C ON U.id=C.user_id
        JOIN projects AS P ON C.project_id=P.id
        GROUP BY U.id)
    AS AV
    SET U.average_score = AV.weight_avg
    WHERE U.id=AV.id;
END
$$
DELIMITER ;
