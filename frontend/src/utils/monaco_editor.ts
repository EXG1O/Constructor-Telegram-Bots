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