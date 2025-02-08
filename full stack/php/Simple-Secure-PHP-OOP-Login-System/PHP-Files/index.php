<?php
require_once 'core/init.php';

if(Session::exists('home')){
	//flash
	echo '<p style="background-color:red;">'. Session::flash('home') .'</p>';
}

$user = new User();
if($user->isLoggedIn()){
?>
<!--page html logado-->


<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="css/image.min.css">
    <title>Home</title>
</head>
<body>
<img class="ui avatar image" src="<?php echo $user->getAvatar() ?>">
<span><a href="profile.php?user=<?php echo escape($user->data()->username); ?>"><?php echo escape($user->data()->username); ?></a></span>
	
	<ul>
		<li><a href="logout.php">Logout</a></li>
		<li><a href="update.php">Atualizar Detalhes</a></li>
		<li><a href="avatar.php">Atualizar Avatar</a></li>
		<li><a href="changepassword.php">Mudar Senha</a></li>
	</ul>
	
</body>
	
	
	
	
	
	
	
<!--fim html-->
<?php	

	if($user->hasPermission('admin')){
		echo '<p>You are an administrator!</p>';
	}

}else{
	?>
	<!--page html deslogado-->
	<p>Faça <a href="login.php">login</a> ou <a href="register.php">registro</a> pra usar o site</p>
	<!--fim html-->
	<?php
}