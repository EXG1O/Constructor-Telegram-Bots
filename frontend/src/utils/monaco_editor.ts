import monaco from 'monaco-editor';

export function updateEditorLayout(
	monacoEditor: monaco.editor.IStandaloneCodeEditor,
	shouldResetWidth: boolean = false,
): void {
	const monacoEditorModel: monaco.editor.ITextModel | null = monacoEditor.getModel();

	if (monacoEditorModel === null) {
		throw new Error('Unable to retrieve Monaco Editor model!');
	}

	monacoEditor.layout({
		width: shouldResetWidth ? 0 : monacoEditor.getContainerDomNode().getBoundingClientRect().width,
		height: monacoEditorModel.getLineCount() * 19,
	});
}

export const defaultEditorOptions: monaco.editor.IStandaloneEditorConstructionOptions = {
	minimap: { enabled: false },
	renderLineHighlight: 'none',
	lineNumbersMinChars: 3,
	overviewRulerLanes: 0,
	scrollBeyondLastLine: false,
	scrollbar: { vertical: 'hidden' },
	inlayHints: { enabled: 'off' },
}