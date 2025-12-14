<?php
require_once 'core/init.php';

if(Session::exists('home')){
	//flash
	echo '<p style="background-color:red;">'. Session::flash('home') .'</p>';
}

if(Input::exists()){
	if(Token::check(Input::get('token'))){
		$validate = new Validate();
		$validation = $validate->check($_POST, array(
			'username' => array('required' => true),
			'password' => array('required' => true)
		));
		
		if($validation->passed()){
			$user = new User();
			
			$remember = (Input::get('remember') === 'on') ? true : false;
			
			$login = $user->login(Input::get('username'), Input::get('password'), $remember);
			
			if($login){
				Redirect::to('index.php');
			}else{
				Session::flash('home', 'Incorrect Username or Password');
				Redirect::to('login.php');
			}
			
		}else{
			echo '<p style="background-color:red;">';
			
			foreach($validation->errors() as $error){
				echo $error, "<br>";
			}
			
			echo "</p>";
		}
	}
}
?>

<form action="" method="post">
	<div class="field">
		<label for="username">Usuário</label>
		<input type="text" name="username" id="username" autocomplete="off">
	</div>
	
	<div class="field">
		<label for="password">Senha</label>
		<input type="password" name="password" id="password" autocomplete="off">
	</div>
	
	<div class="field">
		<label for="remember">
			<input type="checkbox" name="remember" id="remember">Lembrar conexão
		</label>
	</div>
	
	<input type="hidden" name="token" value="<?php echo Token::generate(); ?>">
	<input type="submit" value="Login">
</form>