<?php
    // Startet eine Session
    session_start();

    // Setzt alle bekannten Seiten in einen Array
    $validSites = ["home", "t", "g"];

    // Setzt die Seite fall nicht festgelegt oder unbekannt auf Home
    if (empty($_SESSION['site']) || !in_array($_SESSION['site'], $validSites)) {
        $_SESSION['site'] = "home";
    }
    // Setzt die Seite auf die sich im Get-Parameter befindende Seite
    if (!empty($_GET["site"]) && in_array($_GET["site"], $validSites)) {
        $_SESSION['site'] = $_GET["site"];
    }
?>
<html lang="DE">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./css/grafik.css">
    <link rel="stylesheet" href="./css/Table.css">
    <script src="./js/nav.js"></script>
    <title>REST Statistiken</title>
    <?php
        echo '<link rel="stylesheet" href="./css/site.css">';
    ?>
</head>
<header>
    <nav>
        <ul>
            <?php
            /*
                Rendert die Navigation um eine Aktiv Style setzten zu können.
             */
            if ($_SESSION['site'] == "t") {
                echo '<li><button id="t" class="nav active">Tabelle</button></li>
                              <li><button id="g" class="nav">Graph</button></li>';
            } elseif ($_SESSION['site'] == "g") {
                echo '<li><button id="t" class="nav">Tabelle</button></li>
                              <li><button id="g" class="nav active">Graph</button></li>';
            } else {
                echo '<li><button id="t" class="nav active">Tabelle</button></li>
                              <li><button id="g" class="nav">Graph</button></li>';
            }
            ?>
        </ul>
    </nav>
    <br/>
</header>
<body>
<main>
    <?php
    /*
     * Rendert die gewünschte Seite in den Main-Tag
     */
    if ($_SESSION['site'] == "home") {
        echo file_get_contents("./pages/graph.html");
    } elseif ($_SESSION['site'] == "t") {
        echo file_get_contents("./pages/Table.html");
    } elseif ($_SESSION['site']== "g") {
        echo file_get_contents("./pages/graph.html");
    } else {
       echo file_get_contents("./pages/graph.html");
    }
    ?>
</main>
</body>
</html>
