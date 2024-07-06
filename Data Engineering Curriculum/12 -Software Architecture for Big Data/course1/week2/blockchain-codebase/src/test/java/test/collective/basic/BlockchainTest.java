package test.collective.basic;

import io.collective.basic.Block;
import io.collective.basic.Blockchain;
import org.junit.Before;
import org.junit.Test;

import java.lang.reflect.Field;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;

import static io.collective.basic.Blockchain.mine;
import static junit.framework.TestCase.*;

public class BlockchainTest {
    Blockchain empty = new Blockchain();
    Blockchain one = new Blockchain();
    Blockchain many = new Blockchain();

    @Before
    public void setUp() throws NoSuchAlgorithmException {
        Block genesis = mine(new Block("0", Instant.now().getEpochSecond(), 0));
        Block second = mine(new Block(genesis.getHash(), Instant.now().getEpochSecond(), 0));

        one.add(genesis);
        many.add(genesis);
        many.add(second);
    }

    @Test
    public void isMined() throws NoSuchAlgorithmException {
        Block block = new Block("0", Instant.now().getEpochSecond(), 0);
        Block minedBlock = mine(block);
        assertTrue(Blockchain.isMined(minedBlock));
    }

    @Test
    public void isEmpty() {
        assertTrue(empty.isEmpty());
        assertFalse(one.isEmpty());
        assertFalse(many.isEmpty());
    }

    @Test
    public void size() {
        assertEquals(0, empty.size());
        assertEquals(1, one.size());
        assertTrue(many.size() > 1);
    }

    @Test
    public void isValid() throws NoSuchAlgorithmException {
        assertTrue(empty.isValid());
        assertTrue(one.isValid());
        assertTrue(many.isValid());
    }

    @Test
    public void isNotValid_whenOneIsNotMined() throws NoSuchAlgorithmException {
        Block genesis = new Block("0", Instant.now().getEpochSecond(), 0);

        Blockchain notValid = new Blockchain();
        notValid.add(genesis);

        assertFalse(notValid.isValid());
    }

    @Test
    public void isNotValid_whenManyAreNotMined() throws NoSuchAlgorithmException {
        Block genesis = new Block("0", Instant.now().getEpochSecond(), 0);
        Block second = new Block(genesis.getHash(), Instant.now().getEpochSecond(), 0);

        Blockchain notValid = new Blockchain();
        notValid.add(genesis);
        notValid.add(second);

        assertFalse(notValid.isValid());
    }

    @Test
    public void isNotValid_forIncorrectPreviousHash() throws NoSuchAlgorithmException {
        Block genesis = mine(new Block("0", Instant.now().getEpochSecond(), 0));
        Block second = mine(new Block("anIncorrectHash", Instant.now().getEpochSecond(), 0));

        Blockchain notValid = new Blockchain();
        notValid.add(genesis);
        notValid.add(second);

        assertFalse(notValid.isValid());
    }

    @Test
    public void isValid_HashIncorrect() throws NoSuchAlgorithmException, NoSuchFieldException, IllegalAccessException {
        Blockchain invalid = new Blockchain();
        Block minedBlock = mine(new Block("0", Instant.now().getEpochSecond(), 0));

        Field hashField = minedBlock.getClass().getDeclaredField("hash");
        hashField.setAccessible(true);
        hashField.set(minedBlock, "00 with some mischief");

        invalid.add(minedBlock);

        assertFalse(invalid.isValid());
    }
}
