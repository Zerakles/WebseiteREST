<?php
    session_start();

    $validSites = ["home", "t1", "t2", "g1", "g2"];
    if (empty($_SESSION['site']) || !in_array($_SESSION['site'], $validSites)) {
        $_SESSION['site'] = "home";
    }

    if (!empty($_GET["nav"]) && in_array($_GET["nav"], $validSites)) {
        $_SESSION['site'] = $_GET["nav"];
    }
?>
<html lang="DE">
<head>
    <meta charset="UTF-8"/>
    <link rel="stylesheet" href="./css/site.css">
    <title>REST Statistiken</title>
</head>
<header>
    <nav>
        <ul>
            <?php
            if ($_SESSION['site'] == "t1") {
                echo '<li><button class="nav active">Tabelle PI-1</button></li>
                              <li><button class="nav">Tabelle PI-2</button></li>
                              <li><button class="nav">Graph PI-1</button></li>
                              <li><button class="nav">Graph PI-2</button></li>';
            } elseif ($_SESSION['site'] == "t2") {
                echo '<li><button class="nav">Tabelle PI-1</button></li>
                              <li><button class="active">Tabelle PI-2</button></li>
                              <li><button class="nav">Graph PI-1</button></li>
                              <li><button class="nav">Graph PI-2</button></li>';
            } elseif ($_SESSION['site'] == "g1") {
                echo '<li><button class="nav">Tabelle PI-1</button></li>
                              <li><button class="nav">Tabelle PI-2</button></li>
                              <li><button class="active">Graph PI-1</button></li>
                              <li><button class="nav">Graph PI-2</button></li>';
            } elseif ($_SESSION['site'] == "g22") {
                echo '<li><button class="nav">Tabelle PI-1</button></li>
                              <li><button class="nav">Tabelle PI-2</button></li>
                              <li><button class="nav">Graph PI-1</button></li>
                              <li><button class="active">Graph PI-2</button></li>';
            } else {
                echo '<li><button class="nav">Tabelle PI-1</button></li>
                              <li><button class="nav">Tabelle PI-2</button></li>
                              <li><button class="nav">Graph PI-1</button></li>
                              <li><button class="nav">Graph PI-2</button></li>';
            }
            ?>
        </ul>
    </nav>
</header>
<body>
<main>
    <?php
    if ($_SESSION['site'] == "home") {
        echo '
<section id="main">
    <h2>Willkommen auf der REST Statistikseite!</h2>
    <div class="content">
        <p>Navigiere über die Top-Navigation!</p>
    </div>
</section>';
    } elseif (str_starts_with($_SESSION['site'], "t")) {
        echo file_get_contents("../pages/Table.html");
    } elseif (str_starts_with($_SESSION['site'], "g")) {
        echo file_get_contents("../pages/graph.html");
    } else {
        echo '
<section id="main">
    <h2>Willkommen auf der REST Statistikseite!</h2>
    <div class="content">
        <p>Navigiere über die Top-Navigation!</p>
    </div>
</section>';
    }
    ?>
</main>
</body>
</html>
