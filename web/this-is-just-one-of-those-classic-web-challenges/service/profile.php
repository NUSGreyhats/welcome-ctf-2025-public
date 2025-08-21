<?php

# User profile management
$email = $_POST['email'] ?? '';
$name = $_POST['name'] ?? '';
$age = $_POST['age'] ?? 0;
$location = $_POST['location'] ?? '';
$bio = $_POST['bio'] ?? '';
$newsletter = $_POST['newsletter'] ?? '';
$category = $_POST['category'] ?? 'popular';

$_SESSION['email'] = $email;
$_SESSION['name'] = $name;
$_SESSION['age'] = $age;
$_SESSION['location'] = $location;
$_SESSION['bio'] = $bio;
$_SESSION['newsletter'] = $newsletter;
$_SESSION['category'] = $category;

$db = new SQLite3('app.db');
$stmt = $db->prepare('UPDATE users SET email = ?, display_name = ?, age = ?, location = ?, bio = ?, newsletter = ?, category = ? WHERE id = 1');
$stmt->bindValue(1, $email);
$stmt->bindValue(2, $name);
$stmt->bindValue(3, $age);
$stmt->bindValue(4, $location);
$stmt->bindValue(5, $bio);
$stmt->bindValue(6, $newsletter);
$stmt->bindValue(7, $category);
$stmt->execute();
$stmt->close();
# End of user profile management

# Product display
$user_category = $_SESSION['category'] ?? 'popular';

if ($user_category == 'popular') {
    $name = 'electronics';
} elseif ($user_category == 'trending') {
    $name = 'clothing';
} else {
    error_log("Invalid user category: " . $user_category);
}

$stmt = $db->prepare("SELECT name, price FROM products WHERE category = '$name' LIMIT 10");
$result = $stmt->execute();

$products = [];
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $products[] = $row;
}

$stmt->close();
$db->close();
# End of product display
?>