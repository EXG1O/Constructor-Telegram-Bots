import React, { ReactElement, MouseEvent as ReactMouseEvent, useCallback, useRef, useState } from 'react';
import { Params, json, useRouteLoaderData } from 'react-router-dom';
import ReactFlow, {
	Panel,
	Controls,
	MiniMap,
	Background,
	BackgroundVariant,
	useEdgesState,
	useNodesState,
	addEdge as addEdge_,
	updateEdge,
	NodeTypes,
	MarkerType,
	Connection,
	Node,
	Edge,
} from 'reactflow';

import 'reactflow/dist/style.css';
import './index.scss';

import Button from 'react-bootstrap/Button';

import CommandNode from './components/CommandNode';
import AddCommandOffcanvas from './components/AddCommandOffcanvas';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { TelegramBotCommandDiagramAPI, TelegramBotCommandsDiagramAPI } from 'services/api/telegram_bots/main';
import { TelegramBotCommandDiagram, APIResponse } from 'services/api/telegram_bots/types';

export interface LoaderData {
	diagramCommands: APIResponse.TelegramBotCommandsDiagramAPI.Get;
}

export interface NodeData extends Omit<TelegramBotCommandDiagram, 'x' | 'y'> {
	updateNodes: () => void;
}

export async function loader({ params }: { params: Params<'telegramBotID'> }): Promise<LoaderData | Response> {
	const telegramBotID: number = parseInt(params.telegramBotID!);

	const response = await TelegramBotCommandsDiagramAPI.get(telegramBotID);

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { diagramCommands: response.json };
}

const nodeTypes: NodeTypes = { command: CommandNode };

function Constructor(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;
	const { diagramCommands } = useRouteLoaderData('telegram-bot-menu-constructor') as LoaderData;

	const { createMessageToast } = useToast();

	const [nodes, setNodes, onNodesChange] = useNodesState<NodeData>(parseNodes(diagramCommands));
	const [edges, setEdges, onEdgesChange] = useEdgesState(parseEdges(diagramCommands));
	const edgeUpdating = useRef<Edge | null>(null);

	const [showAddCommandOffcanvas, setAddShowCommandOffcanvas] = useState<boolean>(false);

	function parseNodes(diagramCommands: TelegramBotCommandDiagram[]): Node<NodeData>[] {
		return diagramCommands.map(diagramCommand => {
			const { x, y, ..._diagramCommand } = diagramCommand;

			return {
				id: _diagramCommand.id.toString(),
				type: 'command',
				position: { x, y },
				data: { ..._diagramCommand, updateNodes },
			}
		});
	}

	function parseEdges(diagramCommands: TelegramBotCommandDiagram[]): Edge[] {
		const _edges: Edge[] = [];

		diagramCommands.forEach(diagramCommand => {
			diagramCommand.keyboard?.buttons.forEach(button => {
				if (
					button.telegram_bot_command_id !== null &&
					button.start_diagram_connector !== null &&
					button.end_diagram_connector !== null
				) {
					_edges.push({
						id: `reactflow__edge-${button.start_diagram_connector}-${button.end_diagram_connector}`,
						source: diagramCommand.id.toString(),
						sourceHandle: button.start_diagram_connector,
						target: button.telegram_bot_command_id.toString(),
						targetHandle: button.end_diagram_connector,
					});
				}
			});
		});

		return _edges;
	}

	const updateNodes = useCallback(async (): Promise<void> => {
		const response = await TelegramBotCommandsDiagramAPI.get(telegramBot.id);

		if (response.ok) {
			setNodes(parseNodes(response.json));
			setEdges(parseEdges(response.json));
		} else {
			createMessageToast({
				message: gettext('Не удалось получить данные с сервера!'),
				level: 'danger',
			});
		}
	}, []);

	const handleNodeDragStop = useCallback((event: ReactMouseEvent, node: Node, nodes: Node[] | undefined): void => {
		nodes?.forEach(node => TelegramBotCommandDiagramAPI.updatePosition(
			telegramBot.id,
			parseInt(node.id),
			node.position,
		));
	}, []);

	const addEdge = useCallback(async (
		connection: Connection,
		shouldUpdateEdges: boolean = true,
		showMessageToast: boolean = true,
	): Promise<void> => {
		if (connection.source && connection.sourceHandle && connection.target && connection.targetHandle) {
			const response = await TelegramBotCommandDiagramAPI.connect(
				telegramBot.id,
				parseInt(connection.source),
				{
					telegram_bot_command_id: parseInt(connection.target),
					telegram_bot_command_keyboard_button_id: parseInt(connection.sourceHandle.split(':')[2]),
					start_diagram_connector: connection.sourceHandle,
					end_diagram_connector: connection.targetHandle,
				},
			);

			if (response.ok && shouldUpdateEdges) {
				setEdges(prevEdges => addEdge_(connection, prevEdges));
			}

			if (!response.ok || showMessageToast) {
				createMessageToast({ message: response.json.message, level: response.json.level });
			}
		}
	}, []);

	async function deleteEdge(edge: Edge, shouldUpdateEdges: boolean = true, showMessageToast: boolean = true): Promise<void> {
		if (edge.sourceHandle) {
			const response = await TelegramBotCommandDiagramAPI.disconnect(
				telegramBot.id,
				parseInt(edge.source),
				{ telegram_bot_command_keyboard_button_id: parseInt(edge.sourceHandle.split(':')[2]) },
			);

			if (response.ok && shouldUpdateEdges) {
				setEdges(prevEdges => prevEdges.filter(e => e.id !== edge.id));
			}

			if (showMessageToast) {
				createMessageToast({ message: response.json.message, level: response.json.level });
			}
		}
	}

	const handleEdgeUpdateStart = useCallback((event: ReactMouseEvent, edge: Edge): void => {
		edgeUpdating.current = edge;
	}, []);

	const handleEdgeUpdate = useCallback((oldEdge: Edge, newConnection: Connection): void => {
		if (
			edgeUpdating.current && (
				edgeUpdating.current.sourceHandle !== newConnection.sourceHandle ||
				edgeUpdating.current.targetHandle !== newConnection.targetHandle
			)
		) {
			const showMessageToast = (
				edgeUpdating.current.sourceHandle?.split(':')[2] !== newConnection.sourceHandle?.split(':')[2]
			) || (
				edgeUpdating.current.target !== newConnection.target
			);

			deleteEdge(oldEdge, false, showMessageToast);
			addEdge(newConnection, false, showMessageToast);

			setEdges(prevEdges => updateEdge(oldEdge, newConnection, prevEdges));
		}

		edgeUpdating.current = null;
	}, []);

	const handleEdgeUpdateEnd = useCallback((event: MouseEvent | TouchEvent, edge: Edge): void => {
		if (edgeUpdating.current) {
			deleteEdge(edge);
		}

		edgeUpdating.current = null;
	}, []);

	const handleCheckValidConnection = useCallback((connection: Connection): boolean => {
		if (!(connection.source && connection.sourceHandle && connection.target && connection.targetHandle)) {
			return false;
		}

		if (connection.source === connection.target) {
			return false;
		}

		if (
			edgeUpdating.current && (
				(
					edgeUpdating.current.sourceHandle === connection.sourceHandle
				) || (
					edgeUpdating.current.sourceHandle?.split(':')[1] !== connection.sourceHandle?.split(':')[1] &&
					edgeUpdating.current.sourceHandle?.split(':')[2] === connection.sourceHandle?.split(':')[2]
				)
			)
		) {
			return true;
		}

		for (const edge of edges) {
			if (
				connection.sourceHandle === edge.sourceHandle ||
				connection.sourceHandle?.split(':')[2] === edge.sourceHandle?.split(':')[2]
			) {
				return false;
			}
		}

		return true;
	}, [edges]);

	return (
		<>
			<AddCommandOffcanvas
				show={showAddCommandOffcanvas}
				onAdded={updateNodes}
				onHide={useCallback(() => setAddShowCommandOffcanvas(false), [])}
			/>
			<div className='border rounded' style={{ height: '80vh' }}>
				<ReactFlow
					fitView
					nodes={nodes}
					edges={edges}
					nodeTypes={nodeTypes}
					defaultEdgeOptions={{ markerEnd: { type: MarkerType.Arrow, strokeWidth: 1.8 } }}
					deleteKeyCode={null}
					onNodesChange={onNodesChange}
					onEdgesChange={onEdgesChange}
					onNodeDragStop={handleNodeDragStop}
					onEdgeUpdateStart={handleEdgeUpdateStart}
					onEdgeUpdate={handleEdgeUpdate}
					onEdgeUpdateEnd={handleEdgeUpdateEnd}
					isValidConnection={handleCheckValidConnection}
					onConnect={addEdge}
				>
					<Panel position='top-right'>
						<div className='vstack justify-content-end bg-light border rounded-1 p-1 gap-1'>
							<Button
								size='sm'
								variant='dark'
								onClick={useCallback(() => setAddShowCommandOffcanvas(true), [])}
							>
								{gettext('Добавить команду')}
							</Button>
						</div>
					</Panel>
					<Controls />
					<MiniMap />
					<Background
						variant={BackgroundVariant.Dots}
						size={1}
						gap={24}
					/>
				</ReactFlow>
			</div>
		</>
	);
}

export default Constructor;