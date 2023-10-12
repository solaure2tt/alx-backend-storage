-- SQL script that creates a stored procedure
-- that computes and store the average score for a student
DELIMITER $$ ;
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INTEGER)
BEGIN
	UPDATE users SET average_score = (SELECT AVG(score) AS aver
        				 FROM corrections
        				 WHERE corections.user_id=user_id)
	WHERE id=user_id;
END;$$
DELIMITER ;