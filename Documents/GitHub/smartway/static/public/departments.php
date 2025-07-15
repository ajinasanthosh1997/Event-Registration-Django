<?php
header('Content-Type: application/json');
require __DIR__.'/db.php';

/* Only active depts */
$sql = "
    SELECT 
        dept_id   AS id,
        dept_iname AS name
    FROM tbl_department
    WHERE dept_status = 1
    ORDER BY dept_iname
";
$stmt = $pdo->query($sql);

echo json_encode(['departments' => $stmt->fetchAll(PDO::FETCH_ASSOC)]);
