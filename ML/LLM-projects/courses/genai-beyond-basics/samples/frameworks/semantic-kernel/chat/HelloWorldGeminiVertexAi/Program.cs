﻿using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.Google;

public class Program
{
    const string Location = "us-central1";
    const string ModelId = "gemini-1.5-flash";
    static readonly string ProjectId = Environment.GetEnvironmentVariable("PROJECT_ID") ?? throw new ArgumentNullException("PROJECT_ID environment variable is not set.");

    static readonly string BearerKey = Environment.GetEnvironmentVariable("BEARER_KEY") ?? throw new ArgumentNullException("BEARER_KEY environment variable is not set.");

    static async Task Main()
    {
        // Create a kernel with Google AI's Gemini chat completion
#pragma warning disable SKEXP0070
        var builder = Kernel.CreateBuilder().AddVertexAIGeminiChatCompletion(ModelId, BearerKey, Location, ProjectId);

        // Build the kernel
        Kernel kernel = builder.Build();
        var chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

        // Settings
        GeminiPromptExecutionSettings settings = new()
        {
            Temperature = 0.8,
            MaxTokens = 8192
        };

        // Create a history store the conversation
        var history = new ChatHistory();

        // Initiate a back-and-forth chat
        string? userInput;
        while (true)
        {
            // Collect user input
            Console.Write("User > ");
            userInput = Console.ReadLine();
            if (userInput == null)
            {
                break;
            }

            // Add user input
            history.AddUserMessage(userInput);

            // Get the response from the AI
            var result = await chatCompletionService.GetChatMessageContentAsync(
                history,
                executionSettings: settings,
                kernel: kernel);

            // Print the results
            Console.WriteLine("Assistant > " + result);

            // Add the message from the agent to the chat history
            history.AddMessage(result.Role, result.Content ?? string.Empty);
        }
    }
}