import * as monaco from 'monaco-editor';

export function updateEditorLayout(
	editorDiv: HTMLDivElement,
	monacoEditor: monaco.editor.IStandaloneCodeEditor,
	shouldReset: boolean = false,
): void {
	if (shouldReset) {
		monacoEditor.layout({width: 0, height: 0});
	}

	monacoEditor.layout({
		width: editorDiv.getBoundingClientRect().width,
		height: (monacoEditor.getModel() as monaco.editor.ITextModel).getLineCount() * monacoEditor.getOption(66),
	});
}

export const defaultEditorOptions: monaco.editor.IStandaloneEditorConstructionOptions = {
	minimap: {enabled: false},
	renderLineHighlight: 'none',
	lineNumbersMinChars: 3,
	overviewRulerLanes: 0,
	scrollBeyondLastLine: false,
	scrollbar: {vertical: 'hidden'},
	inlayHints: {enabled: 'off'},
}

export namespace Components {
	export abstract class ListGroupItem {
		public div: HTMLDivElement;
		public editorDiv: HTMLDivElement;
		public monacoEditor!: monaco.editor.IStandaloneCodeEditor;
		public actionButtonsDiv: HTMLDivElement;

		protected constructor(parentElement: HTMLElement, borderColor: string, editorLanguage: string, editorValue?: string) {
			this.div = document.createElement('div');
			this.div.className = 'list-group-item p-3';
			this.div.innerHTML = `
				<div class="d-flex justify-content-between align-items-center gap-3">
					<div class="flex-fill border border-2 border-${borderColor} rounded p-2">
						<div class="editor" style="width: 100%;"></div>
					</div>
					<div class="d-flex btn-action-group gap-2"></div>
				</div>
			`;
			parentElement.appendChild(this.div);

			this.editorDiv = this.div.querySelector('.editor') as HTMLDivElement;
			this.actionButtonsDiv = this.div.querySelector('.btn-action-group') as HTMLDivElement;

			this.createActionButtons();
			this.createEditor(editorLanguage, editorValue);
		}

		protected updateEditorLayout(shouldReset: boolean = false): void {
			updateEditorLayout(this.editorDiv, this.monacoEditor, shouldReset);
		}

		protected onDidChangeEditorContent(): void {
			this.updateEditorLayout();
		}

		protected createEditor(editorLanguage: string, editorValue?: string): void {
			const options = Object.assign(defaultEditorOptions, {value: editorValue || '', language: editorLanguage});

			this.monacoEditor = monaco.editor.create(this.editorDiv, options);
			this.monacoEditor.onDidChangeModelContent(() => this.onDidChangeEditorContent());

			this.updateEditorLayout();
		}

		protected createActionButton(color: string, bootstrapIconName: string): HTMLButtonElement {
			const button = document.createElement('button');
			button.className = `btn btn-${color} bi bi-${bootstrapIconName} px-2 py-0`;
			button.type = 'button';
			button.style.fontSize = '20px';
			return button;
		}

		protected abstract createActionButtons(): void;

		public delete(): void {
			this.div.remove();
		}
	}
}