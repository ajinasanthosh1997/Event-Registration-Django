<?php
/* db.php
 * PDO connector
 */
$DB_HOST = 'localhost';
$DB_NAME = 'smarulmh_smartcrm';
$DB_USER = 'smarulmh_smartcrm';
$DB_PASS = 'feathercode123';

try {
    $pdo = new PDO(
        "mysql:host=$DB_HOST;dbname=$DB_NAME;charset=utf8mb4",
        $DB_USER,
        $DB_PASS,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
} catch (PDOException $e) {
    http_response_code(500);
    echo 'DB connection failed: ' . $e->getMessage();
    exit;
}
