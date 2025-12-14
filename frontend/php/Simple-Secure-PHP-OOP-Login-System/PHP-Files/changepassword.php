<?php
require_once 'core/init.php';

if(Session::exists('home')){
	//flash
	echo '<p style="background-color:red;">'. Session::flash('home') .'</p>';
}

$user = new User();

if(!$user->isLoggedIn()){
	Redirect::to('index.php');
}

if(Input::exists()){
	if(Token::check(Input::get('token'))){
		
		$validate = new Validate();
		$validation = $validate->check($_POST, array(
			'password_current' => array(
				'required' => true,
				'min' => 6
			),
			'password_new' => array(
				'required' => true,
				'min' => 6
			),
			'password_new_again' => array(
				'required' => true,
				'min' => 6,
				'matches' => 'password_new'
			)
		));
		
		if($validation->passed()){
			
			if(Hash::make(Input::get('password_current'), $user->data()->salt) !== $user->data()->password){
				Session::flash('home', 'Sua senha atual está incorreta.');
				Redirect::to('changepassword.php');
			}else{
				$salt = Hash::salt(32);
				$user->update(array(
					'password' => Hash::make(Input::get('password_new'), $salt),
					'salt' => $salt
				));
				
				Session::flash('home', 'Sua senha foi alterada com sucesso.');
				Redirect::to('index.php');
			}
			
		}else{
			echo '<p style="background-color:red;">';
			foreach($validation->errors() as $error){
				echo $error , '<br>';
			}
			echo '</p>';
		}
		
	}
}

?>

<form action="" method="post">
    <div class="field">
        <label for="password_current">Senha atual</label>
        <input type="password" name="password_current" id="password_current">
    </div>

    <div class="field">
        <label for="password_new">Sua nova senha</label>
        <input type="password" name="password_new" id="password_new">
    </div>

    <div class="field">
        <label for="password_new_again">Confirme a nova senha</label>
        <input type="password" name="password_new_again" id="password_new_again">
    </div>

    <input type="submit" value="Mudar">
    <input type="hidden" name="token" value="<?php echo Token::generate(); ?>">
</form>