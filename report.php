<?php
$servername = "";
$username = "";
$password = "";
$dbname = "";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "select CAPACITY, PEERINGS, FACILITIES from SUMMARY";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table><tr><th>Total Peerings</th><th>Total Facilities</th><th>Total Capacity</th></tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>".$row["PEERINGS"]."</td><td>".$row["FACILITIES"]."</td><td>".$row["CAPACITY"]."Gbps</td></tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}


$sql = "select IX_NAME, IX_CITY, IX_COUNTRY, NICE_SPEED from IX order by IX_NAME";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table><tr><th>IX Name</th><th>IX City</th><th>IX Country</th><th>Port Speed</ht></tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>".$row["IX_NAME"]."</td><td>".$row["IX_CITY"]."</td><td>".$row["IX_COUNTRY"]."</td></td><td>".$row["NICE_SPEED"]."</td></tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}
$conn->close();
?>
