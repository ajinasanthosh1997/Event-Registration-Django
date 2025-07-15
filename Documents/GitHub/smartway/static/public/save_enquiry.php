<?php
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method Not Allowed']);
    exit;
}

require __DIR__.'/db.php';

/* ---------- timezone & formatted datetime ---------- */
date_default_timezone_set('Asia/Riyadh');
$datetime = date('d-m-Y h:i:s a');   // e.g. 03-07-2025 10:41:27 am

/* ---------- basic validation ---------- */
$required = [
    'fullname'   => 'Full name is required',
    'cpr'        => 'CPR is required',
    'mobile'     => 'Mobile number is required',
    'department' => 'Department is required',
];

foreach ($required as $key => $msg) {
    if (empty($_POST[$key])) {
        echo json_encode(['status' => 'error', 'message' => $msg]);
        exit;
    }
}

/* optional */
$email   = $_POST['email']   ?? '';
$message = $_POST['message'] ?? '';

/* ---------- insert ---------- */
try {
    $stmt = $pdo->prepare("
        INSERT INTO tbl_enquiry
            (enq_fullname, enq_cpr, enq_mobile, enq_email,
             enq_dept, enq_enqremark, enq_createdatetime,
             enq_publicenquiry, enq_status)
        VALUES
            (:fullname, :cpr, :mobile, :email,
             :dept, :msg, :created,
             1, 5)
    ");

    $stmt->execute([
        ':fullname' => $_POST['fullname'],
        ':cpr'      => $_POST['cpr'],
        ':mobile'   => $_POST['mobile'],
        ':email'    => $email,
        ':dept'     => $_POST['department'],
        ':msg'      => $message,
        ':created'  => $datetime,      
    ]);

    echo json_encode(['status' => 'success']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
}