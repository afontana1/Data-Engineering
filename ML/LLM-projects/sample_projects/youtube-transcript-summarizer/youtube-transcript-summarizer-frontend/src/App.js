import './App.css';
import BackendAPI from './components/BackendApi';
import VideoUploader from './components/Upload';

function App() {
	return (
		<div className="App">
			<header className="App-header">
				<h1>YouTube Transcript Summarizer</h1>
				<pre><div class="line"></div></pre>
				<BackendAPI />
                <VideoUploader />
			</header>
		</div>
	);
}

export default App;
