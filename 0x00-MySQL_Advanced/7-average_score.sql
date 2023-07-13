-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.
-- An average score can be a decimal
-- Create the stored procedure
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(
  IN user_id INT
)
BEGIN
  DECLARE avg_score DECIMAL(10, 2);

  -- Compute the average score
  SELECT AVG(score) INTO avg_score
  FROM corrections
  WHERE corrections.user_id = user_id;

  -- Update the user's average score
  UPDATE users
  SET average_score = avg_score
  WHERE id = user_id;
END $$
DELIMITER ;

