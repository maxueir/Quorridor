def compute_advantages(rewards, values, gamma=0.99, gae_lambda=0.95):
    advantages = []
    gae = 0
    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * values[t+1] - values[t]
        gae = delta + gamma * gae_lambda * gae
        advantages.insert(0, gae)
    return advantages


env = QuoridorEnv()
model = QuoridorPPOCNN()
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
memory = Memory()

for episode in range(1000):
    state = env.reset()
    done = False
    while not done:
        # Sélection d'action
        action_probs, value = model(state)
        dist = Categorical(action_probs)
        action = dist.sample()

        # Exécution dans l'environnement
        next_state, reward, done, _ = env.step(action.item())

        # Stockage dans la mémoire
        memory.states.append(state)
        memory.actions.append(action)
        memory.rewards.append(reward)
        memory.log_probs.append(dist.log_prob(action))

        state = next_state

    # Calcul des avantages et mise à jour
    _, values = model(torch.stack(memory.states))
    advantages = compute_advantages(memory.rewards, values)

    # Loss PPO
    for _ in range(4):  # 4 epochs de mise à jour
        new_action_probs, _ = model(torch.stack(memory.states))
        dist = Categorical(new_action_probs)
        new_log_probs = dist.log_prob(torch.stack(memory.actions))

        ratios = (new_log_probs - torch.stack(memory.log_probs)).exp()
        clipped_ratios = torch.clamp(ratios, 1 - 0.2, 1 + 0.2)

        policy_loss = -torch.min(ratios * advantages, clipped_ratios * advantages).mean()
        value_loss = F.mse_loss(values, torch.tensor(memory.rewards))
        entropy_loss = -dist.entropy().mean()

        loss = policy_loss + 0.5 * value_loss + 0.01 * entropy_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    memory.clear()