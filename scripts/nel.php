nel.php 

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
  </head>
  <body>
  NEL collector endpoint

  <?php file_put_contents('nellogs/NEL.log', file_get_contents('php://input').PHP_EOL, FILE_APPEND); ?>

  </body>
</html>
